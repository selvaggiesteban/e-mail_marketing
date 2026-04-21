# 🚀 E-mail Marketing Automation Suite (V3)

A high-performance, multi-threaded email marketing automation engine designed to maximize deliverability and protect sender reputation through intelligent SMTP rotation and dynamic warm-up strategies.

## 🌟 Key Features (V3)
- **📊 Professional PDF Reporting**: Automatic generation of comprehensive campaign reports using FPDF.
- **📧 Real-time Email Notifications**: Periodic and final status updates sent directly to the administrator, formatted for human readability.
- **🖥️ VPS Gateway Integration**: Includes `vps_gateway.ps1` for seamless deployment to remote Linux servers (Hostinger/VPS) via PowerShell.
- **⚙️ Dynamic Warm-up Engine**: Smart delay cycles (1-10 min) to mimic human behavior and avoid spam filters.
- **🧵 Multi-threaded Execution**: Parallel processing across multiple SMTP accounts for high-volume efficiency.
- **🧪 Mandatory Test Phase**: Automated pre-flight check to verify SMTP health before starting mass distribution.

## 🛠️ Tech Stack
- **Language**: Python 3.12+
- **Core Modules**: `smtplib`, `threading`, `python-dotenv`
- **Reporting**: `fpdf` for PDF generation.
- **Infrastructure**: PowerShell for deployment and gateway management.

## 🚀 Getting Started

### Local Setup
1. **Install Dependencies**:
   ```powershell
   pip install python-dotenv fpdf
   ```
2. **Configure Environment**:
   Clone `.env-example` to `.env` and populate your SMTP credentials and campaign settings.
3. **Run Campaign**:
   ```powershell
   python e-mail_marketing.py
   ```

### VPS Deployment (Hostinger/Linux)
Deploy your campaign to a remote server with a single command:
```powershell
./vps_gateway.ps1
```
The gateway automates:
- Python environment provisioning.
- Secure file transfer (SCP).
- Background execution using `screen` for persistence.

## ⚙️ Configuration (.env)

| Variable | Description |
| :--- | :--- |
| `CAMPAIGN_ID` | Unique identifier for the campaign (e.g., CMP-21042026). |
| `SMTP_ACCOUNTS` | Comma-separated list of accounts in `email|app_password` format. |
| `REPORT_DIRECTORY` | Target folder for PDF and JSON report artifacts. |
| `CONTACT_LIST` | Path to the UTF-8 encoded plain text list of recipients. |
| `MESSAGE` | Path to the Markdown or Text file containing the body. |

## 🛡️ Best Practices & Security
- **App Passwords**: Always use Google App Passwords instead of master passwords.
- **Rate Limiting**: The built-in 1-10 min variable delay is optimized for Gmail's SMTP limits.
- **Encoding**: Ensure `emails.txt` and `message.md` are saved in **UTF-8** (without BOM) to prevent decoding errors.

## 📄 License
This project is for private professional use. All rights reserved.

---
*Developed by Esteban Selvaggi | [selvaggiesteban.dev](https://selvaggiesteban.dev/)*
