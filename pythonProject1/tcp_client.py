import socket
import time

TIMEOUT = 0
N = 10 # The number of iterations of RTT that are calculated.
BUFFER_SIZE = 1024

class TCPClient:

    def __init__(self):
        # NOTE since the public IP address of the EC2 instance changes every time it is started,
        # self.server_name must be updated accordingly.
        self.server_name = '13.40.52.10'
        self.server_port = 5555
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.clientsocket.close()
    
    def connect_to_server(self):
        print('Connecting to server...')
        self.clientsocket.connect((self.server_name, self.server_port))
        print('Connected to server.')
        self.clientsocket.settimeout(TIMEOUT) # Set the client socket to non-blocking so that we can skip
                                              # if there are no messages to receive, instead of waiting.

    def send_server(self, message):
        self.clientsocket.send(message.encode())
    
    def recv_server(self):
        response = ''
        try: # Since the socket is non-blocking, an exception is thrown if there is nothing to receive.
            response = self.clientsocket.recv(BUFFER_SIZE).decode()
        except:
            pass
        return response