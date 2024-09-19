import socket
import termcolor
import threading

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        print(termcolor.colored(("Port Opened " + str(port)), 'green'))
        sock.close()
    except:
        pass

def scan(target, ports):
    print('\n' + ' Starting Scan For ' + str(target))
    for port in range(1, ports + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()

targets = input("Enter IPs To Scan (comma-separated for multiple): ")
ports = int(input("Enter How Many Ports You Want To Scan: "))
if ',' in targets:
    print(termcolor.colored(("Scanning Multiple IPs"), 'green'))
    for ip_addr in targets.split(','):
        scan(ip_addr.strip(' '), ports)
else:
    scan(targets, ports)
