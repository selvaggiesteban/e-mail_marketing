# Gateway para VPS Hostinger
# Configuración extraída de DATOS.MD

$vps_ip = "72.60.59.25"
$vps_user = "root"
$vps_pass = "g(5WWkmj8&9#JsMQ"

function Show-Menu {
    Write-Host "`n--- VPS GATEWAY (Hostinger) ---" -ForegroundColor Cyan
    Write-Host "1. Probar conexión SSH"
    Write-Host "2. Instalar dependencias en VPS (Python, FPDF, Dotenv)"
    Write-Host "3. Desplegar script y archivos"
    Write-Host "4. Iniciar campaña en VPS (Screen)"
    Write-Host "5. Ver logs de campaña"
    Write-Host "Q. Salir"
}

do {
    Show-Menu
    $choice = Read-Host "Seleccione una opción"

    switch ($choice) {
        "1" {
            Write-Host "Probando conexión a $vps_ip..."
            ssh ${vps_user}@${vps_ip} "echo 'Conexión exitosa'"
        }
        "2" {
            Write-Host "Instalando dependencias..."
            ssh ${vps_user}@${vps_ip} "apt update && apt install -y python3 python3-pip screen && pip3 install python-dotenv fpdf"
        }
        "3" {
            Write-Host "Transfiriendo archivos..."
            scp e-mail_marketing.py .env ${vps_user}@${vps_ip}:/root/
            ssh ${vps_user}@${vps_ip} "mkdir -p /root/campaigns"
            # Nota: Esto asume que las carpetas locales existen
            Write-Host "Archivos base transferidos."
        }
        "4" {
            Write-Host "Iniciando campaña en segundo plano..."
            ssh ${vps_user}@${vps_ip} "screen -dmS mailing python3 /root/e-mail_marketing.py"
            Write-Host "Campaña iniciada en sesión 'mailing'."
        }
        "5" {
            ssh ${vps_user}@${vps_ip} "screen -r mailing"
        }
    }
} while ($choice -ne "Q")
