import socket
from IPy import IP

class PortScanner():
    def __init__(self, target: str):
        self.target = target
        self.ip = self.get_ip()
        self.open_ports = []

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
            return socket.gethostbyname(_domain)

    def port_Scanner(self, port: int) -> None:
        try:
            self.sock = socket.socket()
            self.sock.settimeout(0.1)
            self.sock.connect((self.ip, port))
            self.open_ports.append(port)
        except:
            pass

    def scan(self, start_port: int=0, end_port: int=1023) -> None:
        """Range of ports to scan. Start and end ports are inclusive."""
        progress = 0
        end_port = end_port if end_port > start_port else start_port
        scale = 100 / (end_port - start_port + 1)
        for port in range(start_port, end_port + 1):
            progress += scale
            self.port_Scanner(port)
            print(f'\r[{progress:.2f}%]', end='')
        print('\n====================================================')
        print(f'Target: {self.target}')
        print(f'IP: {self.ip}')
        self.open_ports = str(self.open_ports).replace('[', '').replace(']', '')
        print(f'Open ports: {self.open_ports}')

            
def main() -> None:
    target = input('Enter target to scan: ')
    try:
        start_port = int(input('Enter start port: '))
    except ValueError:
        start_port = 0
    try:
        end_port = int(input('Enter end port: '))
    except ValueError:
        end_port = 1023
    PortScanner(target).scan(start_port, end_port)

if __name__ == '__main__':
    main()
