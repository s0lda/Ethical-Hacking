import socket
import os
import tqdm

HOST = '127.0.0.1'
PORT = 5822

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(1)
client, addr = sock.accept()


while True:
    header = client.recv(1024).decode()
    command = input(header).encode()

    if command == b'':
        print('>> ')
    else:
        client.send(command)
        data = client.recv(1024).decode('utf8')
        if data == 'exit':
            print(f'Connection terminated: {addr[0]}')
            break
        print(data)
        
client.close()
sock.close()
