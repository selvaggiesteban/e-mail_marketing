# 🚀 E-mail Marketing Automation (SMTP Multi-account)

Este es un potente script de automatización para campañas de E-mail Marketing desarrollado en Python. Está diseñado para realizar envíos masivos de forma inteligente, utilizando múltiples cuentas SMTP en paralelo y una estrategia de "warm-up" para proteger la reputación de los dominios y evitar bloqueos.

## ✨ Características Principales

- **📦 Procesamiento Paralelo**: Distribuye la carga de contactos entre múltiples cuentas de Gmail simultáneamente usando `threading`.
- **📈 Estrategia de Warm-up Dinámica**: Implementa ciclos de retraso incrementales y decrementales (1-10-1 minutos) para imitar el comportamiento humano y cuidar la salud de tus cuentas.
- **🧪 Fase de Validación**: Sistema de envío de prueba obligatorio con espera de aprobación manual antes de iniciar la distribución masiva.
- **📊 Reportes Inteligentes**:
    - Generación automática de reportes en formato JSON cada 10 minutos.
    - Envío de reporte final al terminar la campaña.
    - Notificaciones de estado enviadas directamente a tu bandeja de entrada.
- **⚙️ Configuración Descentralizada**: Gestión total mediante variables de entorno (`.env`).

## 🛠️ Requisitos Técnicos

- Python 3.8+
- Cuentas de Gmail con "Contraseñas de Aplicación" activadas.
- Dependencias:
  - `python-dotenv`

## 🚀 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/e-mail-marketing.git
   cd e-mail-marketing
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install python-dotenv
   ```

3. Configura tus credenciales:
   ```bash
   cp .env-example .env
   # Edita el archivo .env con tus datos reales
   ```

## ⚙️ Configuración (.env)

El script se apoya totalmente en el archivo `.env` para su funcionamiento:

| Variable | Descripción |
| :--- | :--- |
| `CAMPAIGN_ID` | Identificador único de la campaña. |
| `SUBJECT` | Asunto del correo electrónico. |
| `CONTACT_LIST` | Ruta al archivo `.txt` con la lista de destinatarios. |
| `MESSAGE` | Ruta al archivo `.md` o `.txt` con el cuerpo del mensaje. |
| `TEST_RECIPIENT` | Email donde recibirás las pruebas y reportes. |
| `SMTP_ACCOUNTS` | Lista de cuentas en formato `email|password` separadas por comas. |

## 📈 Estrategia de Envío (Warm-up)

Para maximizar la entregabilidad, el script alterna los tiempos de espera entre envíos de la siguiente manera:
`1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2` minutos por cada cuenta.

Este ciclo se repite automáticamente, permitiendo un flujo constante pero seguro de salida de correos.

## 📊 Formato de Reporte

Cada 10 minutos recibirás un reporte con la siguiente estructura:

```json
{
    "reporte": {
        "fecha_reporte": "YYYY-MM-DD HH:MM:SS",
        "fecha_campana": "YYYY-MM-DD HH:MM:SS",
        "id_campana": "ID-XXX",
        "estado_campana": "En progreso/Completada",
        "asunto": "...",
        "enviadas": "XX",
        "entregados": "XX"
    },
    "audiencia": {
        "listas_incluidas": "path/to/list.txt"
    }
}
```

## 🤝 Contacto

Desarrollado por **Esteban Selvaggi** - [selvaggiesteban.dev](https://selvaggiesteban.dev/)

---
*Nota: Este script está destinado únicamente a fines de marketing ético y profesional. Asegúrate de cumplir con las leyes locales (como RGPD) y las políticas de servicio de tu proveedor SMTP.*
