import socket
from IPy import IP

target = input('Enter target to scan: ')

def find_ip(target: str) -> str:
    try:
        IP(target)
        return target
    except ValueError:
        # gethostbyname() takes only domain as argument.
        # need get domain only from supplied url.
        domain = target.replace('http://', '').replace('https://', '')
        _domain = ''
        for i in domain:
            if i == '/':
                break
            else:
                _domain += i
        return socket.gethostbyname(_domain)

def port_Scanner(ip: str, port: int) -> None:
    port += 1
    try:
        sock = socket.socket()
        sock.settimeout(0.1)
        sock.connect((ip, port))
        print(f'Port {port} is open.')
    except:
        print(f'Port {port} is closed.')

ip = find_ip(target)

for port in range(0, 1023):
    scanner = port_Scanner(ip, port)
