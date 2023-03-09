#script for if we are using pygame
#this script will be run on the client side, and will send data to the server
#this script will be modified based on which computer it is running on - player 1's , or player 2's
#this version is for player 1

import socket
import time
from main import *

server_name = '18.133.159.31'
server_port = 12000
client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect((server_name, server_port))

#variables are defined in game code, which this script will have access to
#i have predicted following variables: btn_press, x_position, user_score, user_lives
#there will be more which i can easily add or remove unnecessary variavles

while True:

    #concanete all the data into one string called user1data
    client_socket1.send(player1lives.encode())
    player2lives = client_socket1.recv(1024).decode()

    #wait a small while before sending more data. this will send info about users actions 10 times per second.
    time.sleep(0.1)                                                                                                                                             