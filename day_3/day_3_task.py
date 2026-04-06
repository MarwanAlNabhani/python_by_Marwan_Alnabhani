import csv
import json
from datetime import datetime

def is_valid_log_line(line):
    # Basic required keywords
    required_keywords = ["ACCEPT", "DROP", "SRC=", "DST=", "SPT=", "DPT=", "LEN="]

    # Check action exists
    if not any(action in line for action in ["ACCEPT", "DROP"]):
        return False

    # Check all required fields exist
    for keyword in required_keywords[2:]:
        if keyword not in line:
            return False

    return True

def parse_log_line(line):
    parts = line.strip().split()

    # Extract timestamp (first 5 parts)
    timestamp = " ".join(parts[0:5])

    # Extract action and protocol
    action = parts[5]
    protocol = parts[6]

    # Extract key=value pairs
    data = {}
    for item in parts[7:]:
        if "=" in item:
            key, value = item.split("=")
            data[key] = value

    return {
        "timestamp": timestamp,
        "action": action,
        "protocol": protocol,
        "source_ip": data.get("SRC"),
        "source_port": data.get("SPT"),
        "destination_ip": data.get("DST"),
        "destination_port": data.get("DPT"),
        "packet_size": data.get("LEN")
    }

def find_suspicious_ips(ip_counts):
    suspicious = {}

    for ip, count in ip_counts.items():
        if count >= 3:
            suspicious[ip] = count

    return suspicious

def get_top_ports(port_counts, top_n=3):
    # Convert dictionary to list of tuples and sort
    sorted_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_ports[:top_n]

def save_to_csv(entries, filename="output/output.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        # Header
        writer.writerow([
            "Timestamp", "Action", "Protocol",
            "Source IP", "Source Port",
            "Destination IP", "Destination Port",
            "Packet Size"
        ])

        # Rows
        for e in entries:
            writer.writerow([
                e["timestamp"],
                e["action"],
                e["protocol"],
                e["source_ip"],
                e["source_port"],
                e["destination_ip"],
                e["destination_port"],
                e["packet_size"]
            ])

def save_to_json(entries, filename="output/output.json"):
    with open(filename, "w") as file:
        json.dump(entries, file, indent=4)


def save_threat_report(suspicious_ips, filename="output/threats.txt"):
    with open(filename, "w") as file:
        file.write("THREAT REPORT - Generated: " + str(datetime.now()) + "\n")
        file.write("=" * 50 + "\n")
        file.write("Suspicious IPs (3+ log appearances):\n")

        for ip, count in suspicious_ips.items():
            file.write(f"IP: {ip} | Occurrences: {count}\n")

def print_summary(total, valid, malformed,
                  accept_count, drop_count,
                  top_ports, suspicious_ips):

    print("=" * 60)
    print("  FIREWALL LOG ANALYSIS REPORT")
    print("=" * 60)

    print(f"Total entries processed : {total}")
    print(f"Valid entries parsed    : {valid}")
    print(f"Malformed entries skipped: {malformed}")
    print()

    # --- Action Summary ---
    print("---  Action Summary ---")
    print(f"  ACCEPT : {accept_count}")
    print(f"  DROP   : {drop_count}")
    print()

    # --- Top Ports ---
    print("---  Top 3 Targeted Destination Ports ---")
    for i, (port, count) in enumerate(top_ports, start=1):
        print(f"  {i}. Port {port} — {count} hits")
    print()

    # --- Suspicious IPs ---
    print("---  Suspicious Source IPs (3+ appearances) ---")
    if suspicious_ips:
        for ip, count in suspicious_ips.items():
            print(f"  {ip} — {count} occurrences")
    else:
        print("  None")
    print()

    print("Output saved:")
    print("  output.csv")
    print("  output.json")
    print("  threats.txt")
    print("=" * 60)

def main():
    parsed_entries = []

    accept_count = 0
    drop_count = 0

    port_counts = {}
    ip_counts = {}

    valid_count = 0
    malformed_count = 0
    total_count = 0

    with open("firewall.log", "r") as file:
        for line in file:
            total_count += 1

            if not is_valid_log_line(line):
                malformed_count += 1
                continue

            entry = parse_log_line(line)
            parsed_entries.append(entry)
            valid_count += 1

            # Action count
            if entry["action"] == "ACCEPT":
                accept_count += 1
            else:
                drop_count += 1

            # Destination port count
            port = entry["destination_port"]
            if port in port_counts:
                port_counts[port] += 1
            else:
                port_counts[port] = 1

            # Source IP count
            ip = entry["source_ip"]
            if ip in ip_counts:
                ip_counts[ip] += 1
            else:
                ip_counts[ip] = 1

    suspicious_ips = find_suspicious_ips(ip_counts)  
    top_ports = get_top_ports(port_counts)

    save_to_csv(parsed_entries)
    save_to_json(parsed_entries)
    save_threat_report(suspicious_ips)

    print_summary(
    total_count,
    valid_count,
    malformed_count,
    accept_count,
    drop_count,
    top_ports,
    suspicious_ips
    )

    print("Processing complete.")


if __name__ == "__main__":
    main()