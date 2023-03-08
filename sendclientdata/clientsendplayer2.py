#script for if we are using pygame
#this script will be run on the client side, and will send data to the server
#this script will be modified based on which computer it is running on - player 1's , or player 2's
#this version is for player 2

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

    #conditional updates - only send update to server if change is registered, to save latency as these dont need to be sent 10 times a second if theyre usually the same
    if player2_lives == player2_lives-1:
        client_socket.send(player_lives.encode())

    else if #space invader is destroyed by this player:
        client_socket.send(#space invader is destroyed.encode())
    
    else if #bullet shot by this player:
        client_socket.send(#bullet shot.encode())
    

    #concatenate automatically sent game data into a string
    auto_game_data = f'{player2_x_position}|{player2_score}'

    # send variable values to server
    client_socket.send(auto_game_data.encode())


    #get updates on all non local variables from server
    player1_lives = client_socket.recv(1024).decode()
    player1_score = client_socket.recv(1024).decode()
    player1_x_position = client_socket.recv(1024).decode()
    base_lives = client_socket.recv(1024).decode()


    
    #wait a small while before sending more data. this will send info about users actions 10 times per second.
    time.sleep(0.1)

                                                                                                                                                                