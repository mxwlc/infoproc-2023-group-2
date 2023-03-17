import socket

from game_server_logic.game_server import *

port = 5555
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind(('0.0.0.0', port))

tcpserver.settimeout(0)

tcpserver.listen(2)

game_server = GameServer()

# Wait for two clients to connect
clients = []
while len(clients) < 2:
    try:
        client, address = tcpserver.accept()
        clients.append(client)
        print(f"Client {len(clients)} connected from {address}")
    except:
        continue

# Start the game loop
while True:
        
        try:
            client1_incoming = clients[0].recv(1024)
        except:
            client1_incoming = ''

        try:
            client2_incoming = clients[1].recv(1024)
        except:
            client2_incoming = ''
        
        client1_outgoing, client2_outgoing = game_server.update(client1_incoming, client2_incoming)
        if client1_outgoing != '':
            clients[0].send(client1_outgoing)
        if client2_outgoing != '':
            clients[1].send(client2_outgoing)