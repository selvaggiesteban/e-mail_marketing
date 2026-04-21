# 🚀 E-mail Marketing Automation Suite (V3)

Sistema avanzado de automatización para e-mail marketing diseñado para maximizar la entregabilidad mediante el uso de múltiples cuentas SMTP de Gmail en paralelo y estrategias inteligentes de warm-up.

## 🌟 Novedades en V3
- **📊 Generación de Reportes PDF**: Al finalizar cada campaña, se genera automáticamente un reporte visual profesional.
- **📧 Reportes Legibles**: Notificaciones de estado vía email formateadas para lectura humana.
- **🖥️ VPS Gateway**: Script puente para despliegue y gestión remota en servidores Hostinger/Linux.
- **📂 Gestión de Archivos**: Carpeta de reportes personalizable mediante variables de entorno.

## ✨ Características Principales
- **📦 Multi-threading**: Distribución inteligente de contactos entre múltiples cuentas SMTP.
- **📈 Ciclo de Warm-up Dinámico**: Estrategia de retrasos de 1 a 10 minutos para proteger la reputación del remitente.
- **🧪 Fase de Pruebas**: Validación obligatoria con envío de prueba antes de la distribución masiva.
- **⏱️ Tracking de Tiempos**: Registro preciso del inicio y fin de cada campaña.

## 🛠️ Requisitos Técnicos
- Python 3.12+
- Dependencias: `python-dotenv`, `fpdf`
- Cuentas de Gmail con "App Passwords" habilitadas.

## 🚀 Instalación y Despliegue

### Local
1. Instala dependencias:
   ```powershell
   pip install python-dotenv fpdf
   ```
2. Configura tu `.env` (usa `.env-example` como base).
3. Ejecuta:
   ```powershell
   python e-mail_marketing.py
   ```

### VPS (Hostinger)
Utiliza el gateway de PowerShell incluido para automatizar el despliegue:
```powershell
./vps_gateway.ps1
```
Este script permite:
- Instalar Python y dependencias en el VPS.
- Transferir archivos locales al servidor.
- Ejecutar la campaña en segundo plano usando `screen`.

## ⚙️ Configuración (.env)
| Variable | Descripción |
| :--- | :--- |
| `CAMPAIGN_ID` | ID único de la campaña (ej: CMP-21042026). |
| `REPORT_DIRECTORY` | Carpeta donde se guardarán los PDFs generados. |
| `SMTP_ACCOUNTS` | Cuentas SMTP en formato `email|password,email|password`. |
| `TEST_RECIPIENT` | Email que recibe pruebas y reportes finales. |

## 🤝 Contacto
Desarrollado por **Esteban Selvaggi** - [selvaggiesteban.dev](https://selvaggiesteban.dev/)
