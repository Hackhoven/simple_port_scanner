import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from common_ports import COMMON_PORTS

def validate_host(target_host):
    try:
        ipaddress.ip_address(target_host)
        return True
    except ValueError:
        pass
    
    try:
        ipaddress.ip_interface(target_host)
        return True
    except ValueError:
        pass

    return False

def scan_port(target_host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target_host, port))
            
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"Port {port} ({service}) is open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def scan_ports(target_host, max_threads=20):
    if not validate_host(target_host):
        print("Invalid target host. Please enter a valid IP address or hostname.")
        return
    
    print(f"Scanning ports for {target_host}...")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(1, 500):
            executor.submit(scan_port, target_host, port)

if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    scan_ports(target_host)
