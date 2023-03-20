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
public_ips = []
private_ips = []

def check_connection(msg1, msg2):
    client1_disc = False
    client2_disc = False
    if msg1 == 'x':
        client1_disc = True
        print('Client 1 disconnected.')
        if len(clients) == 2:
            print('    client 2 -> client 1')
    if msg2 == 'x':
        client2_disc = True
        print('Client 2 disconnected.')
    if client1_disc and client2_disc:
        clients.clear()
        public_ips.clear()
        private_ips.clear()
    elif client1_disc:
        clients.pop(0)
        public_ips.pop(0)
        private_ips.pop(0)
    elif client2_disc:
        clients.pop(1)
        public_ips.pop(1)
        private_ips.pop(1)
    return client1_disc or client2_disc

while True:

    print('Waiting for clients...')

    while len(clients) < 2:

        if len(clients) == 1:
            msg = ''
            try:
                msg = clients[0].recv(1024).decode()
            except:
                pass
            check_connection(msg, '')

        try:
            client, address = tcpserver.accept()
            local_ip = client.recv(1024).decode()
            private_ips.append(local_ip)
            client.settimeout(0)
            clients.append(client)
            public_ips.append(address[0])
            print(f"Client {len(clients)} connected from public IP {address}, private IP {local_ip}.")
        except:
            continue

    game_server.init_clients(public_ips, private_ips)

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

            if check_connection(client1_incoming, client2_incoming):
                break
            
            client1_outgoing, client2_outgoing = game_server.update(client1_incoming, client2_incoming)
            if client1_outgoing != '':
                clients[0].send(client1_outgoing.encode())
            if client2_outgoing != '':
                clients[1].send(client2_outgoing.encode())