#Hackhoven's port scanner

import socket
import re
import threading


def validate_host(target_host):
    try:
        socket.inet_aton(target_host)   #validate IP
        return True
    
    except socket.error:
        pass


    if re.match(r'^[a-zA-Z0-9.-]+$', target_host):
        return True
    
    return False


def scan_port(target_host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target_host, port))

        if result == 0:
            print(f"Port {port} is open")

        s.close()
    
    except socket.error as e:
        print(f"Socket error: {e}")

    except socket.gaierror as ge:
        print(f"Hostname resolution error: {ge}")

    except Exception as err:
        print(f"Error occurred: {err}")


def scan_ports(target_host):
    
    if not validate_host(target_host):
        print("Invalid target host. Please enter a valid IP address or hostname.")
        return

    threads = []
    for port in range(1, 65536):
        thread = threading.Thread(target=scan_port, args=(target_host, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    scan_ports(target_host)
