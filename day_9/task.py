import subprocess
import platform
import json
import yaml
import smtplib
from email.message import EmailMessage
from datetime import datetime
import ipaddress
import os
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

NETWORK = os.getenv("NETWORK")
OUTPUT_DIR = "./reports"

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# =========================
# CREATE OUTPUT DIRECTORY
# =========================
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PING FUNCTION
# =========================
def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", str(ip)]

    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

# =========================
# SCAN NETWORK
# =========================
def scan_network(network):
    results = []

    for ip in ipaddress.ip_network(network, strict=False):
        ip_str = str(ip)
        status = "up" if ping(ip_str) else "down"

        print(f"{ip_str} is {status}")

        results.append({
            "ip": ip_str,
            "status": status
        })

    return results

# =========================
# SAVE REPORT
# =========================
def save_report(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    json_file = os.path.join(OUTPUT_DIR, f"scan_{timestamp}.json")
    yaml_file = os.path.join(OUTPUT_DIR, f"scan_{timestamp}.yaml")

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    with open(yaml_file, "w") as f:
        yaml.dump(data, f)

    return json_file, yaml_file

# =========================
# SEND EMAIL
# =========================
def send_email(json_file, yaml_file):
    msg = EmailMessage()
    msg["Subject"] = "Network Scan Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content("Attached are the latest network scan reports.")

    for file in [json_file, yaml_file]:
        with open(file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file)
            )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Email failed: {e}")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, NETWORK]):
        raise ValueError("Missing required environment variables!")

    scan_results = {
        "timestamp": datetime.now().isoformat(),
        "network": NETWORK,
        "hosts": scan_network(NETWORK)
    }

    json_file, yaml_file = save_report(scan_results)
    send_email(json_file, yaml_file)

    print("Scan completed successfully.")