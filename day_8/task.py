from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
import os

# List of devices
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.2",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "ip": "10.0.0.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "juniper_junos",
        "ip": "192.168.1.3",
        "username": "admin",
        "password": "password"
    }
]

# Ensure backup directory exists
backup_dir = "./backups"
os.makedirs(backup_dir, exist_ok=True)

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

for device in devices:
    ip = device["ip"]
    device_type = device["device_type"]
    net_connect = None

    print(f"\nAttempting to connect to {ip} ({device_type})...")

    try:
        # Connect to device
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {ip}.")

        # Get hostname
        if "cisco" in device_type:
            hostname = net_connect.send_command("show running-config | include hostname")
            hostname = hostname.split()[-1]
            config = net_connect.send_command("show running-config")

        elif "juniper" in device_type:
            hostname = net_connect.send_command("show configuration system host-name")
            hostname = hostname.split()[-1].strip(";")
            config = net_connect.send_command("show configuration")

        else:
            hostname = ip  # fallback if unknown device
            config = net_connect.send_command("show running-config")

        print(f"Device Hostname: {hostname}")
        print(f"Retrieving running configuration from {hostname}...")

        # Create filename
        filename = f"{hostname}_{current_date}.txt"
        filepath = os.path.join(backup_dir, filename)

        # Save configuration
        with open(filepath, "w") as file:
            file.write(config)

        print(f"Configuration backup for {hostname} saved to {filepath} successfully.")

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Error backing up configuration for {ip}: {str(e)}")

    except Exception as e:
        print(f"Unexpected error with {ip}: {str(e)}")

    finally:
        if net_connect:
            net_connect.disconnect()
        print(f"Disconnected from {ip}.")