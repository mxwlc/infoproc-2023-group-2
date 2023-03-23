### This script simulates a typical game by sending messages to the server in place of the game script.
### The server responses and RTT are recorded.

import socket
import time

# Connect to server.
server_name = '13.40.52.10'
server_port = 5555
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((server_name, server_port))
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((server_name, server_port))
clients = []
clients.append(client1)
clients.append(client2)

start_time = 0

# Send client i a message.
def send(i, message, display=True):
    global start_time
    start_time = time.time()
    clients[i - 1].send(message.encode())
    if display:
        print(str(i) + ' sent ' + message)

def recv(i, display=True, rtt=True):
    response = clients[i - 1].recv(1024).decode()
    delta = time.time() - start_time
    if display:
        print(str(i) + ' received ' + response)
        print('    RTT = ' + str(delta) + 's')
    return response

# Test request for leaderboard.
send(1, 'l')
recv(1)

# Start game.
send(1, 'rone', False)
send(2, 'rtwo', False)
print('Sent notifications of readiness')
r1 = recv(1, False)
r2 = recv(2, False)
print('1 received ' + r1 + ', 2 received ' + r2)

# Wait for enemy bullet.
r1 = recv(1, False)
r2 = recv(2, False)
print('1 received ' + r1 + ', 2 received ' + r2)

# Send test messages to server.
requests = ['10.1', 'c', 'm', 'c', 'b1', 'c', 'e1', 'p', 'g20:30'] # Note that all requests are sent from client 1.
who_receives = [1,   1,   1,   1,   1,    1,   2,    2,   0]      # 0: neither client receives response.
                                                                  # 1: only other client receives response. 
                                                                  # 2: both clients receive response.
for i in range(len(requests)):
    send(1, requests[i])
    if who_receives[i] == 1:
        recv(2)
    elif who_receives[i] == 2:
        r1 = recv(1, True, False)
        r2 = recv(2, True, False)
        print

# Close connection to server.
client1.send('x'.encode())
client1.close()
client2.send('x'.encode())
client2.close()