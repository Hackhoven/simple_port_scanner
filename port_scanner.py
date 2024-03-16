# Hackhoven's port scanner

import socket
import re
from concurrent.futures import ThreadPoolExecutor

#COMMON_PORTS = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080]

def validate_host(target_host):
    try:
        socket.inet_aton(target_host)   #validate IP
        return True
    except socket.error:
        pass

    if re.match(r'^[a-zA-Z0-9.-]+$', target_host):
        return True
    return False

def scan_port(target_host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target_host, port))
            if result == 0:
                service_name = socket.getservbyport(port)
                print(f"Port {port} ({service_name}) is open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def scan_ports(target_host, max_threads=20, timeout=1):
    if not validate_host(target_host):
        print("Invalid target host. Please enter a valid IP address or hostname.")
        return

    print(f"Scanning ports for {target_host}...")
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        #for port in COMMON_PORTS:
        for port in range(1, 1000):
            executor.submit(scan_port, target_host, port, timeout)

if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    scan_ports(target_host)
