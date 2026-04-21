import os
import time
import smtplib
import json
import threading
import datetime
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from fpdf import FPDF

# Cargar variables de entorno
load_dotenv()

CAMPAIGN_ID = os.getenv("CAMPAIGN_ID", "N/A")
CAMPAIGN_NAME = os.getenv("CAMPAIGN_NAME", "Sin Nombre")
SUBJECT = os.getenv("SUBJECT", "Sin Asunto")
CONTACT_LIST_PATH = os.getenv("CONTACT_LIST", "contacts.txt")
MESSAGE_PATH = os.getenv("MESSAGE", "message.md")
TEST_RECIPIENT = os.getenv("TEST_RECIPIENT", "")
SMTP_ACCOUNTS_RAW = os.getenv("SMTP_ACCOUNTS", "")
REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", ".")

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
    "inicio_campana": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "fin_campana": "N/A"
}
stats_lock = threading.Lock()

def get_delays():
    cycle = list(range(1, 11)) + list(range(9, 1, -1))
    while True:
        for d in cycle:
            yield d

def send_email(account, recipient, subject, body, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = account['email']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(account['email'], account['password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando desde {account['email']} a {recipient}: {e}")
        return False

def generate_pdf_report():
    if not os.path.exists(REPORT_DIRECTORY):
        os.makedirs(REPORT_DIRECTORY)
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte Final de Campaña", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID Campaña: {CAMPAIGN_ID}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre: {CAMPAIGN_NAME}", ln=True)
    pdf.cell(200, 10, txt=f"Asunto: {SUBJECT}", ln=True)
    pdf.cell(200, 10, txt=f"Inicio: {stats['inicio_campana']}", ln=True)
    pdf.cell(200, 10, txt=f"Fin: {stats['fin_campana']}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Contactos: {stats['total_contactos']}", ln=True)
    pdf.cell(200, 10, txt=f"Enviados: {stats['enviadas']}", ln=True)
    pdf.cell(200, 10, txt=f"Entregados: {stats['entregados']}", ln=True)
    pdf.cell(200, 10, txt=f"Errores: {stats['errores']}", ln=True)
    
    filename = f"reporte_{CAMPAIGN_ID}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(REPORT_DIRECTORY, filename)
    pdf.output(filepath)
    return filepath

def send_report(final=False):
    global stats
    with stats_lock:
        if final:
            stats["fin_campana"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stats["estado"] = "Completada"
            
        report_data = {
            "reporte": {
                "fecha_reporte": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fecha_inicio": stats["inicio_campana"],
                "fecha_fin": stats["fin_campana"],
                "id_campana": CAMPAIGN_ID,
                "estado_campana": stats["estado"],
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
    
    # Cuerpo del email formateado para humanos
    report_body = f"""
==========================================
   REPORTE DE CAMPAÑA - {CAMPAIGN_ID}
==========================================
Estado: {stats['estado']}
Asunto: {SUBJECT}
------------------------------------------
DETALLES DE ENVÍO:
- Total Contactos: {stats['total_contactos']}
- Enviados: {stats['enviadas']}
- Entregados: {stats['entregados']}
- Errores: {stats['errores']}
------------------------------------------
TIEMPOS:
- Inicio: {stats['inicio_campana']}
- Fin: {stats['fin_campana']}
- Reporte: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
------------------------------------------
AUDIENCIA:
- Lista: {CONTACT_LIST_PATH}
==========================================
"""

    pdf_path = None
    if final:
        pdf_path = generate_pdf_report()
        print(f"Reporte PDF generado: {pdf_path}")

    report_acc = next((acc for acc in SMTP_ACCOUNTS if acc['email'] == TEST_RECIPIENT), SMTP_ACCOUNTS[0] if SMTP_ACCOUNTS else None)
    
    if report_acc:
        subject = f"REPORTE {'FINAL' if final else 'ESTADO'} - Campaña {CAMPAIGN_ID}"
        send_email(report_acc, TEST_RECIPIENT, subject, report_body, attachment_path=pdf_path)

def reporter_thread():
    while stats["estado"] == "En progreso":
        time.sleep(600)
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
        
        if contact != contacts[-1]:
            delay = next(delay_gen)
            print(f"[{account['email']}] [{status_msg}] {contact}. Esperando {delay} min...")
            time.sleep(delay * 60)
        else:
            print(f"[{account['email']}] [{status_msg}] {contact}. Finalizado.")

# Cargar mensaje y contactos
try:
    with open(MESSAGE_PATH, 'r', encoding='utf-8') as f:
        campaign_message = f.read()
    with open(CONTACT_LIST_PATH, 'r', encoding='utf-8') as f:
        all_contacts = [line.strip() for line in f if line.strip()]
    stats["total_contactos"] = len(all_contacts)
except Exception as e:
    print(f"Error cargando archivos: {e}")
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

num_accounts = len(SMTP_ACCOUNTS)
chunk_size = (len(all_contacts) + num_accounts - 1) // num_accounts
contact_chunks = [all_contacts[i:i + chunk_size] for i in range(0, len(all_contacts), chunk_size)]

stats["estado"] = "En progreso"
print(f"Iniciando campaña con {num_accounts} cuentas y {len(all_contacts)} contactos...")

threading.Thread(target=reporter_thread, daemon=True).start()

threads = []
for i in range(num_accounts):
    if i < len(contact_chunks):
        t = threading.Thread(target=worker, args=(SMTP_ACCOUNTS[i], contact_chunks[i]))
        t.start()
        threads.append(t)

for t in threads:
    t.join()

send_report(final=True)
print("Campaña finalizada.")
