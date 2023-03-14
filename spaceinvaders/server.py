import socket
from game_server_logic import *

port = 5555
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind(('0.0.0.0', port))

tcpserver.settimeout(0)

tcpserver.listen(2)

create_leaderboard()

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
            player1lives = clients[0].recv(1024)
            clients[1].send(player1lives)
            print("sent player 1 lives to client 2")
        except:
            continue

        try:
            player2lives = clients[1].recv(1024)
            clients[0].send(player2lives)
            print("sent player 2 lives to client 1")
        except:
            continue
