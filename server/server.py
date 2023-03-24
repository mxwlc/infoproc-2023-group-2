# Run this script on the EC2 instance to start the server.

import socket
import atexit

from game_server_logic.game_server import *

TIMEOUT = 0
BUFFER_SIZE = 1024

# Create a welcome socket.
port = 5555
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind(('0.0.0.0', port))
tcpserver.listen(2)
tcpserver.settimeout(TIMEOUT)

game_server = GameServer()

# Wait for two clients to connect.
clients = []
ips = []

# If the server crashes, close all sockets for a smoother disconnection.
def exit_handler():
    tcpserver.close()
    for client in clients:
        client.close()

atexit.register(exit_handler)

# Check if one or both of the clients have disconnected, and if so, remove them from the lists of clients/ips.
def check_connection(client_incoming, crash_game):
    client_disc = [False, False]
    for i in range(2):
        client_disc[i] = client_incoming[i] == 'x' or crash_game
        # Remove client if a) they have left out-of-game or b) one of the clients has left in-game.
    if client_disc[0] and client_disc[1]:
        clients.clear()
        ips.clear()
        print('Both clients disconnected.')
    elif client_disc[0]:
        clients.pop(0)
        ips.pop(0)
        print('Client 1 disconnected.')
        if len(clients) == 1: # If client 1 disconnects, then client 2 becomes client 1
                              # (clients are identified by their positions in the list)
            print('    (Client 2 is now client 1.)')
    elif client_disc[1]:
        clients.pop(1)
        ips.pop(1)
        print('Client 2 disconnected.')

# Main program loop
while True:

    # Check to see if we can accept a new client.
    if len(clients) < 2:
        try:
            client, address = tcpserver.accept()
            client.settimeout(TIMEOUT)
            clients.append(client)
            ips.append(address[0])
            print(f"Client {len(clients)} connected from {address}.")
        except:
            pass
    
    client_incoming = ['', '']

    # Receive messages from clients.
    for i in range(2):
        try:
            client_incoming[i] = clients[i].recv(BUFFER_SIZE).decode()
            # Note that this statement throws two types of exceptions:
            # 1. We are connected to client 1 but have no new messages to receive.
            # 2. We are not connected to client 1.
        except:
            pass
        
    # Update server with incoming messages, and generate outgoing messages.
    client_outgoing, crash_game = game_server.update(client_incoming, ips)

    # Send messages to clients.
    for i in range(2):
        # Do not send an empty string.
        if client_outgoing[i] != '':
            try:
                clients[i].send(client_outgoing[i].encode())
            except:
                pass
    
    check_connection(client_incoming, crash_game)

## OLD ##

# Main program loop
# while True:

#     print('Waiting for clients...')

#     # Wait until 2 clients have connected.
#     while len(clients) < 2:

#         if len(clients) == 1:
#             msg = ''
#             try:
#                 msg = clients[0].recv(BUFFER_SIZE).decode()
#             except:
#                 pass
#             check_connection(msg, '')

#         client, address = tcpserver.accept()
#         client.settimeout(TIMEOUT)
#         clients.append(client)
#         ips.append(address[0])
#         print(f"Client {len(clients)} connected from {address}.")

#     # When 2 clients have connected, start the main game loop.
#     while True:
            
#             client1_incoming = ''
#             try:
#                 client1_incoming = clients[0].recv(BUFFER_SIZE).decode()
#             except:
#                 pass

#             client2_incoming = ''
#             try:
#                 client2_incoming = clients[1].recv(BUFFER_SIZE).decode()
#             except:
#                 pass

#             if check_connection(client1_incoming, client2_incoming):
#                 break
            
#             # Update server with incoming messages, and generate outgoing messages.
#             client1_outgoing, client2_outgoing = game_server.update(client1_incoming, client2_incoming)
#             # Do not send an empty string.
#             if client1_outgoing != '':
#                 clients[0].send(client1_outgoing.encode())
#             if client2_outgoing != '':
#                 clients[1].send(client2_outgoing.encode())