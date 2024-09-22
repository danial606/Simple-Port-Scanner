import socket
import termcolor
import threading

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
        
        sock.close()
    except socket.timeout:
        print(termcolor.colored(f"Timeout on port {port}", 'red'))
    except socket.error:
        print(termcolor.colored(f"Error connecting to port {port}", 'red'))

def scan(target, start_port, end_port):
    print(f'\n Starting Scan For {target}')
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()

targets = input("Enter IPs To Scan (comma-separated for multiple): ")
port_range = input("Enter port range to scan (e.g. 20-80): ")

start_port, end_port = map(int, port_range.split('-'))

if ',' in targets:
    print(termcolor.colored("Scanning Multiple IPs", 'green'))
    for ip_addr in targets.split(','):
        scan(ip_addr.strip(), start_port, end_port)
else:
    scan(targets, start_port, end_port)
