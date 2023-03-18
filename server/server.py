import socket

from game_server_logic.game_server import *

port = 5555
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind(('0.0.0.0', port))

tcpserver.settimeout(0)

tcpserver.listen(2)

game_server = GameServer()

print ('Waiting for clients...')

# Wait for two clients to connect
clients = []
ips = []
while len(clients) < 2:
    try:
        client, address = tcpserver.accept()
        client.settimeout(0)
        clients.append(client)
        ips.append(address[0])
        print(f"Client {len(clients)} connected from {address}")

        # if len(clients) == 1:
        #     client.send('l'.encode())
        #     print('Set listener')
        # else:
        #     client.send(('c' + ips[0]).encode())
        #     print('Set connector')
    except:
        continue

game_server.init_clients(ips)

# Start the game loop
while True:
        
        client1_incoming = ''
        try:
            client1_incoming += clients[0].recv(1024).decode()
        except:
            pass

        client2_incoming = ''
        try:
            client2_incoming += clients[1].recv(1024).decode()
        except:
            pass
        
        client1_outgoing, client2_outgoing = game_server.update(client1_incoming, client2_incoming)
        if client1_outgoing != '':
            clients[0].send(client1_outgoing.encode())
        if client2_outgoing != '':
            clients[1].send(client2_outgoing.encode())