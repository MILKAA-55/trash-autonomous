import socket
import json
import threading
import time

class RobotNetworkClient:
    def __init__(self, host="192.168.4.1", port=8888, on_data_received=None):
        self.host = host
        self.port = port
        self.on_data_received = on_data_received
        self.socket = None
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._connect_loop, daemon=True).start()

    def _connect_loop(self):
        while self.running:
            try:
                print(f"[PC] Connexion au robot sur {self.host}:{self.port}...")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                print("[PC] Connecté au Robot-Poubelle avec succès !")
                
                buffer = b""
                while self.running:
                    chunk = self.socket.recv(1024)
                    if not chunk:
                        break
                    buffer += chunk
                    
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        if line.strip():
                            packet = json.loads(line.decode('utf-8'))
                            if self.on_data_received:
                                self.on_data_received(packet)
                                
            except Exception as e:
                print(f"[PC] Déconnecté ou erreur : {e}. Nouvelle tentative dans 3s...")
                if self.socket:
                    self.socket.close()
                time.sleep(3)

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()