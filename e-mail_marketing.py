import os
import time
import smtplib
import json
import threading
import datetime
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Cargar variables de entorno
load_dotenv()

CAMPAIGN_ID = os.getenv("CAMPAIGN_ID", "N/A")
CAMPAIGN_NAME = os.getenv("CAMPAIGN_NAME", "Sin Nombre")
SUBJECT = os.getenv("SUBJECT", "Sin Asunto")
CONTACT_LIST_PATH = os.getenv("CONTACT_LIST", "contacts.txt")
MESSAGE_PATH = os.getenv("MESSAGE", "message.md")
TEST_RECIPIENT = os.getenv("TEST_RECIPIENT", "")
SMTP_ACCOUNTS_RAW = os.getenv("SMTP_ACCOUNTS", "")

# Procesar cuentas SMTP
SMTP_ACCOUNTS = []
if SMTP_ACCOUNTS_RAW:
    for acc in SMTP_ACCOUNTS_RAW.split(","):
        if "|" in acc:
            email, password = acc.split("|")
            SMTP_ACCOUNTS.append({"email": email, "password": password})

# Estado global de la campaña
stats = {
    "enviadas": 0,
    "entregados": 0,
    "errores": 0,
    "total_contactos": 0,
    "estado": "Iniciando",
    "inicio_campana": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
stats_lock = threading.Lock()

def get_delays():
    # Ciclo: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2
    cycle = list(range(1, 11)) + list(range(9, 1, -1))
    while True:
        for d in cycle:
            yield d

def send_email(account, recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = account['email']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(account['email'], account['password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando desde {account['email']} a {recipient}: {e}")
        return False

def send_report(final=False):
    global stats
    with stats_lock:
        report_data = {
            "reporte": {
                "fecha_reporte": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fecha_campana": stats["inicio_campana"],
                "id_campana": CAMPAIGN_ID,
                "estado_campana": "Completada" if final else stats["estado"],
                "asunto": SUBJECT,
                "enviadas": str(stats["enviadas"]),
                "entregados": str(stats["entregados"]),
            },
            "audiencia": {
                "listas_incluidas": CONTACT_LIST_PATH
            },
        }
    
    report_json = json.dumps(report_data, indent=4)
    print(f"\n--- REPORTE {'FINAL' if final else 'PERIODICO'} ---\n{report_json}\n")
    
    # Enviar reporte por email
    # Intentar encontrar la cuenta que coincide con TEST_RECIPIENT
    report_acc = next((acc for acc in SMTP_ACCOUNTS if acc['email'] == TEST_RECIPIENT), SMTP_ACCOUNTS[0] if SMTP_ACCOUNTS else None)
    
    if report_acc:
        subject = f"REPORTE {'FINAL' if final else 'ESTADO'} - Campaña {CAMPAIGN_ID}"
        # Según instrucciones: usar {destinatario_prueba} como remitente y destinatario
        send_email(report_acc, TEST_RECIPIENT, subject, report_json)

def reporter_thread():
    while stats["estado"] == "En progreso":
        time.sleep(600) # 10 minutos
        if stats["estado"] == "En progreso":
            send_report()

def worker(account, contacts):
    global stats
    delay_gen = get_delays()
    
    for contact in contacts:
        contact = contact.strip()
        if not contact: continue
        
        success = send_email(account, contact, SUBJECT, campaign_message)
        
        with stats_lock:
            stats["enviadas"] += 1
            if success:
                stats["entregados"] += 1
                status_msg = "EXITO"
            else:
                stats["errores"] += 1
                status_msg = "FALLO"
        
        if contact != contacts[-1]: # No esperar después del último
            delay = next(delay_gen)
            print(f"[{account['email']}] [{status_msg}] {contact}. Esperando {delay} min...")
            time.sleep(delay * 60)
        else:
            print(f"[{account['email']}] [{status_msg}] {contact}. Finalizado.")

# Cargar mensaje
try:
    with open(MESSAGE_PATH, 'r', encoding='utf-8') as f:
        campaign_message = f.read()
except Exception as e:
    print(f"Error cargando mensaje: {e}")
    sys.exit(1)

# Cargar contactos
try:
    with open(CONTACT_LIST_PATH, 'r', encoding='utf-8') as f:
        all_contacts = [line.strip() for line in f if line.strip()]
    stats["total_contactos"] = len(all_contacts)
except Exception as e:
    print(f"Error cargando contactos: {e}")
    sys.exit(1)

if not SMTP_ACCOUNTS:
    print("No hay cuentas SMTP configuradas.")
    sys.exit(1)

# Fase de Prueba
print("Iniciando fase de prueba...")
for acc in SMTP_ACCOUNTS:
    print(f"Enviando prueba desde {acc['email']}...")
    send_email(acc, TEST_RECIPIENT, f"[PRUEBA] {SUBJECT}", campaign_message)

print("\nPruebas enviadas a", TEST_RECIPIENT)
confirm = input("¿Desea comenzar la distribución de la campaña? (s/n): ")
if confirm.lower() != 's':
    print("Campaña cancelada.")
    sys.exit(0)

# Dividir contactos
num_accounts = len(SMTP_ACCOUNTS)
chunk_size = (len(all_contacts) + num_accounts - 1) // num_accounts
contact_chunks = [all_contacts[i:i + chunk_size] for i in range(0, len(all_contacts), chunk_size)]

stats["estado"] = "En progreso"
print(f"Iniciando campaña con {num_accounts} cuentas y {len(all_contacts)} contactos...")

# Iniciar hilo de reportes
threading.Thread(target=reporter_thread, daemon=True).start()

# Iniciar trabajadores
threads = []
for i in range(num_accounts):
    if i < len(contact_chunks):
        t = threading.Thread(target=worker, args=(SMTP_ACCOUNTS[i], contact_chunks[i]))
        t.start()
        threads.append(t)

for t in threads:
    t.join()

stats["estado"] = "Completada"
send_report(final=True)
print("Campaña finalizada.")
