import socket

class TCPClient:

    def __init__(self):
        self.server_name = '18.133.242.186'
        self.server_port = 5555
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.server_name, self.server_port))
        self.clientsocket.settimeout(0)
    
    def send(self, message):
        self.clientsocket.send(message.encode())
    
    def recv(self):
        return self.clientsocket.recv(1024).decode()