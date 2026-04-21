# 🚀 E-mail Marketing Automation Suite

The ultimate high-performance engine for precision email marketing. This suite is engineered to bypass common deliverability hurdles using multi-account orchestration, human-mimicking behavior, and automated bounce management.

## 📌 Overview
This automation suite allows businesses to scale their outreach by distributing campaigns across multiple Gmail accounts. It handles the complexities of SMTP rate limits, sender reputation, and real-time bounce tracking automatically.

## ⚡ Core Capabilities
*   **Orchestrated Delivery**: Intelligent distribution of contacts across multiple SMTP accounts in parallel.
*   **Reputation Shield**: Dynamic "warm-up" delay cycles (1 to 10 minutes) to keep your accounts under the radar of spam filters.
*   **🔍 Automated Bounce Scanning**: Integrated IMAP engine that scans your inboxes for "MAILER-DAEMON" notifications to identify dead emails.
*   **🌍 Bilingual Detection**: Supports permanent failure detection in both **English and Spanish** (e.g., "Address not found" / "Dirección no encontrada").
*   **Hybrid Deployment**: Run locally for quick tasks or deploy to a VPS using the built-in PowerShell Gateway.
*   **Smart Reporting**: Human-readable status updates via email and professional PDF generation for audits.

## 🛠 Project Architecture
*   **Engine**: Python 3.12+ (Multi-threaded worker system).
*   **Communication**: SMTP_SSL for sending and IMAP_SSL for bounce scanning.
*   **Security**: Full `.env` integration and `.gitignore` protection for sensitive data.

## 🚦 Getting Started

### 1. Installation
```powershell
pip install python-dotenv fpdf
```

### 2. Configuration
Create a `.env` file based on the provided example. Add your Gmail accounts using **App Passwords** (Ensure IMAP is enabled in your Gmail settings).

### 3. Execution
The system will run a mandatory test phase before starting the full campaign. After the sending phase, it will automatically scan all inboxes for bounces.
```powershell
python e-mail_marketing.py
```

## 📊 Campaign Artifacts
After every campaign, the system organizes data into:
*   **Reports**: Visual PDFs and detailed JSON logs with specialized "Bounce" metrics.
*   **Logs**: Real-time console output showing connection status and scanning progress.

---
*Developed by Esteban Selvaggi | [selvaggiesteban.dev](https://selvaggiesteban.dev/)*
