import socket

class TCPClient:

    def __init__(self):
        self.server_name = '100.26.250.2'
        self.server_port = 5555
        self.peer_port = 5556
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket = None

    def close(self):
        self.clientsocket.close()
        self.peer_socket.close()
    
    def connect_to_server(self):
        print('Connecting to server...')
        self.clientsocket.connect((self.server_name, self.server_port))
        print('Connected to server.')
        self.clientsocket.send(socket.gethostbyname(socket.gethostname()).encode())
        print('Sent private IP.')
        self.clientsocket.settimeout(0)
    
    def listen_for_peer(self):
        welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcome_socket.bind(('0.0.0.0', self.peer_port))
        welcome_socket.settimeout(0)
        welcome_socket.listen(1)
        print('Listening for peer...')
        while True:
            try:
                self.peer_socket, address = welcome_socket.accept()
                break
            except:
                pass
        print('Found peer.')
        welcome_socket.close()
    
    def connect_to_peer(self, ips):
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO see if there is a better way of connecting to peers on the same network.
        # Currently, it tries to connect via both the public and private ips, which doesn't
        # feel like the best solution.
        try:
            print('Searching for peer via public IP...')
            self.peer_socket.connect((ips[0], self.peer_port))
            # Try public IP first
        except:
            print('Searching for peer via private IP...')
            self.peer_socket.connect((ips[1], self.peer_port))
            # If public IP doesn't work, try private IP
        print('Found peer.')
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