import socket
import time

TIMEOUT = 0
N = 10 # The number of iterations of RTT that are calculated.

class TCPClient:

    def __init__(self):
        self.server_name = '18.130.146.140'
        self.server_port = 5555
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.clientsocket.close()
    
    def connect_to_server(self):
        print('Connecting to server...')
        self.clientsocket.connect((self.server_name, self.server_port))
        print('Connected to server.')
        self.clientsocket.settimeout(TIMEOUT)

    def send_server(self, message):
        self.clientsocket.send(message.encode())
    
    def recv_server(self):
        response = ''
        try:
            response += self.clientsocket.recv(1024).decode()
        except:
            pass
        return response