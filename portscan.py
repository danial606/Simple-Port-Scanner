import socket
import termcolor
import threading
from tqdm import tqdm
import ipaddress

open_ports = []

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        
        try:
            banner = sock.recv(1024).decode().strip()
            print(termcolor.colored(f"Port {port} Open: {banner}", 'green'))
        except:
            print(termcolor.colored(f"Port {port} Open, but no banner received", 'green'))
        
        open_ports.append(port)
        sock.close()
    except socket.timeout:
        print(termcolor.colored(f"Timeout on port {port}", 'red'))
    except socket.error:
        print(termcolor.colored(f"Error connecting to port {port}", 'red'))

def scan(target, start_port, end_port):
    print(f'\n Starting Scan For {target}')
    
    for port in tqdm(range(start_port, end_port + 1), desc=f"Scanning Ports on {target}"):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()

targets = input("Enter IPs To Scan (comma-separated for multiple): ")
port_range = input("Enter port range to scan (e.g. 20-80): ")

start_port, end_port = map(int, port_range.split('-'))

if ',' in targets:
    print(termcolor.colored("Scanning Multiple IPs", 'green'))
    for ip_addr in targets.split(','):
        ip_addr = ip_addr.strip()
        if is_valid_ip(ip_addr):
            open_ports.clear() 
            scan(ip_addr, start_port, end_port)
            print(f"\nScan completed for {ip_addr}. Open ports: {open_ports}")
        else:
            print(termcolor.colored(f"Invalid IP address: {ip_addr}", 'red'))
else:
    if is_valid_ip(targets):
        open_ports.clear() 
        scan(targets, start_port, end_port)
        print(f"\nScan completed for {targets}. Open ports: {open_ports}")
    else:
        print(termcolor.colored("Invalid IP address", 'red'))
