import socket

class TCPClient:

    def __init__(self):
        self.server_name = 'localhost'
        self.server_port = 5555
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.clientsocket.connect((self.server_name, self.server_port))
        self.clientsocket.settimeout(0)
    
    def send(self, message):
        self.clientsocket.send(message.encode())
    
    def recv(self):
        try:
            response = self.clientsocket.recv(1024).decode()
            return response
        except:
            return ''