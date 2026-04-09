import nmap
from netmiko import ConnectHandler
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================

devices = [
    {"ip": "192.168.1.1", "device_type": "cisco_ios"},
    {"ip": "192.168.1.2", "device_type": "cisco_ios"},
]

USERNAME = "admin"
PASSWORD = "admin123"

# ==============================
# NMAP SCAN FUNCTION
# ==============================

def scan_device(ip):
    scanner = nmap.PortScanner()
    result = {
        "ip": ip,
        "telnet_port": False,
        "http_port": False
    }

    try:
        scanner.scan(ip, "23,80")

        if ip in scanner.all_hosts():
            ports = scanner[ip]["tcp"]

            if 23 in ports and ports[23]["state"] == "open":
                result["telnet_port"] = True

            if 80 in ports and ports[80]["state"] == "open":
                result["http_port"] = True

    except Exception as e:
        print(f"[!] Nmap scan failed for {ip}: {e}")

    return result

# ==============================
# NETMIKO AUDIT FUNCTION
# ==============================

def audit_device(ip, device_type):
    result = {
        "telnet_config": "Unknown",
        "http_config": "Unknown",
        "snmp_config": "Unknown"
    }

    device = {
        "device_type": device_type,
        "host": ip,
        "username": USERNAME,
        "password": PASSWORD,
    }

    try:
        connection = ConnectHandler(**device)

        # Telnet check
        telnet_output = connection.send_command(
            "show running-config | include line vty|transport input"
        )

        if "telnet" in telnet_output.lower():
            result["telnet_config"] = "Telnet is enabled"
        else:
            result["telnet_config"] = "Telnet is disabled"

        # HTTP check
        http_output = connection.send_command(
            "show running-config | include ip http"
        )

        if "ip http server" in http_output and "no ip http server" not in http_output:
            result["http_config"] = "HTTP server is enabled"
        else:
            result["http_config"] = "HTTP server is disabled"

        # SNMP check
        snmp_output = connection.send_command(
            "show running-config | include snmp-server community"
        )

        if "public" in snmp_output.lower() or "private" in snmp_output.lower():
            result["snmp_config"] = "Default SNMP community strings found"
        else:
            result["snmp_config"] = "No default SNMP community strings found"

        connection.disconnect()

    except Exception as e:
        print(f"[!] Connection failed for {ip}: {e}")
        result["telnet_config"] = "Connection failed"
        result["http_config"] = "Connection failed"
        result["snmp_config"] = "Connection failed"

    return result

# ==============================
# MAIN FUNCTION
# ==============================

def main():
    results = []

    print("[*] Starting network audit...\n")

    for device in devices:
        ip = device["ip"]
        device_type = device["device_type"]

        print(f"[*] Scanning {ip}...")

        scan_result = scan_device(ip)
        audit_result = audit_device(ip, device_type)

        results.append({
            "device": ip,
            "telnet_status": audit_result["telnet_config"],
            "http_status": audit_result["http_config"],
            "snmp_status": audit_result["snmp_config"],
            "telnet_port_open": scan_result["telnet_port"],
            "http_port_open": scan_result["http_port"]
        })

    # Generate report file
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"Audit_Report_{date_str}.txt"

    with open(filename, "w") as file:
        file.write("--- Network Device Audit Report ---\n\n")

        for r in results:
            file.write(f"Device: {r['device']}\n")
            file.write(f"  - Telnet Status: {r['telnet_status']}\n")
            file.write(f"  - HTTP Server Status: {r['http_status']}\n")
            file.write(f"  - SNMP Status: {r['snmp_status']}\n\n")

    print(f"\n[+] Audit report saved to {filename}")

# ==============================
# RUN SCRIPT
# ==============================

if __name__ == "__main__":
    main()