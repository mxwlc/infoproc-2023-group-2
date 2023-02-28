import socket
import time

server_name = #servername
server_port = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_name, server_port))

#variables are defined in game code, which this script will have access to
#i have predicted following variables: btn_press, x_position, user_score, user_lives
#there will be more which i can easily add or remove unnecessary variavles

while True:

    #concatenate variables into one big string
    game_data = f'{btn_press}|{x_position}|{user_score}|{user_lives}'

    # send variable values to server using UDP as faster
    client_socket.sendall(game_data.encode())
    
    #wait a small while before sending more data. this will send info about users actions 10 times per second.
    time.sleep(0.1)