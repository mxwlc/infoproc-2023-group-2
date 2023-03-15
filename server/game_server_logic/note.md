# Server-side game logic interface

## game_server.py

- This file contains a class GameServer that is responsible for all server-side game logic. The file should be imported into the TCP server, the class should be instantiated using the default constructor, and update should be called on a loop.
- The update function in GameServer is the only function needed to interface with the class, aside from the constructor. It takes the raw TCP messages from both clients as strings, and returns a tuple of the two messages to send back to the clients, as strings.

## create_leaderboard.py

- This file should be run once on the EC2 instance after starting it to set up the database.
- Currently, create_leaderboard is set up to run every time a new GameServer instance is instantiated. This is a matter of convenience, and could be improved in the future.

## leaderboard_functions.py

- This file provides functions which allow GameServer to access the database in an easy way. It does not need to be interfaced with directly by anything other than game_server.py.