# Server

This folder contains all server-side logic, including the TCP server, game server logic, and DynamoDB interfaces.

- server.py: the main python script that runs on the EC2 instance. It calls/instantiates all other functions/classes needed.
- testing.py: a program that simulates two clients connected to the server and playing the game. It should be run on a local machine.
- game_server_logic: all game logic and the DyanamoDB interfaces. See game_server_logic/note.md for more details.