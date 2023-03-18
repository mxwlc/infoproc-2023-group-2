import socket

class TCPClient:

    def __init__(self):
        self.server_name = '52.91.132.54'
        self.server_port = 5555
        self.peer_port = 5556
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket = None
    
    def connect_to_server(self):
        self.clientsocket.connect((self.server_name, self.server_port))
        self.clientsocket.settimeout(0)
    
    def listen_for_peer(self):
        welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcome_socket.bind(('0.0.0.0', self.peer_port))
        welcome_socket.settimeout(0)
        welcome_socket.listen(1)
        while True:
            try:
                self.peer_socket, address = welcome_socket.accept()
                break
            except:
                pass
    
    def connect_to_peer(self, ip):
        print(ip)
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.connect(('localhost', self.peer_port))
        # TODO find a way to connect via the parameter ip.
        # The issue likely has something to do with the difference between public and private IP addresses.
        self.peer_socket.settimeout(0)

    def send_server(self, message):
        self.clientsocket.send(message.encode())
    
    def recv_server(self):
        response = ''
        try:
            response += self.clientsocket.recv(1024).decode()
        except:
            pass
        return response
    
    def send_peer(self, message):
        self.peer_socket.send(message.encode())

    def recv_peer(self):
        response = ''
        try:
            response += self.peer_socket.recv(1024).decode()
        except:
            pass
        return response