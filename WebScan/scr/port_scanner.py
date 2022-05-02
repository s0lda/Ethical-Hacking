import socket
from IPy import IP
import time

class PortScanner():
    def __init__(self, target: str):
        self.target = target
        self.ip = self.get_ip()

    def get_ip(self) -> str:
        try:
            IP(self.target)
            return self.target
        except ValueError:
            # gethostbyname() takes only domain as argument.
            # need get domain only from supplied url.
            domain = self.target.replace('http://', '').replace('https://', '')
            _domain = ''
            for i in domain:
                if i == '/':
                    break
                else:
                    _domain += i
            try:
                return socket.gethostbyname(_domain)
            except socket.gaierror:
                print('Invalid domain name.')
                exit()

    def scan_port(self, port: int) -> bool:
        try:
            self.sock = socket.socket()
            self.sock.settimeout(0.1)
            self.sock.connect((self.ip, port))
            print(f'{port} is open.')
            return True
        except:
            print(f'{port} is closed.')
            pass
        return False
