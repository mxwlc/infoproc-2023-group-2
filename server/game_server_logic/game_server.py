import time
import random

from game_server_logic.leaderboard_functions import *
from game_server_logic.create_leaderboard import *

NUM_ENEMIES = 44
SCORE_INCREMENT = 10 # How much a player's score should increase by upon killing an enemy.
ENEMY_BULLET_INTERVAL = 2 # Time in seconds between spawnings of enemy bullets.

class GameServer:

    # The game state is reset in two situations:
    # 1. The game server object is initialised.
    # 2. The game ends.
    def reset_game_state(self):
        self.player_ready = [False, False]
        self.player_name = ['', '']
        self.player_score = [0, 0]
        self.player_bullets = [False, False] # Whether or not there exists a bullet for each player.
        self.game_in_progress = False
        self.remaining_enemies = []
        for i in range(NUM_ENEMIES):
            self.remaining_enemies.append(True)
        self.killed_enemies = 0 # The number of enemies that have been killed; when this reaches 
                                # the total number of enemies, spawn a new wave.
        self.enemy_bullet = False # Whether or not there exists an enemy bullet.
        print('Reset game state.')

    def __init__(self):
        try:
            create_leaderboard()
            print('Created new leaderboard.')
            # Although create_leaderboard does not need to be called every time a new game instance is started,
            # it makes things easier to do it this way and has very little extra cost.
        except:
            pass
        self.reset_game_state()

    def start_game(self):
        self.game_in_progress = True
        self.game_time = time.time()
        self.elapsed_time = 0
        self.time_since_bullet = 0
        print('Started game.')
    
    def end_game(self):
        for i in range(2): # Update leaderboard with both players' names and scores.
            update_leaderboard(self.player_name[i], self.player_score[i])
        self.reset_game_state()
        print('Ended game.')
    
    # Parses messages if the game is in progress.
    # Return messages: messages to return to the client that sent the incoming (raw) message.
    # Relay messages: messages to relay to the other client.
    def parse_ingame(self, client_index, raw_message, return_messages, relay_messages):
        messages = raw_message.split(';')
        sent_position = False
        for m in messages: # TODO consider iterating backwards through messages
            if len(m) == 0: # Empty messages or trailing ;
                pass
            elif m[0].isdigit(): # Player position
                if sent_position:
                    pass
                else:
                    relay_messages.append(m)
                    sent_position = True
            elif m == 'c': # Player bullet creation
                relay_messages.append(m)
                self.player_bullets[client_index] = True
                print('Player ' + str(client_index + 1) + ' created bullet.')
            elif m == 'm': # Player bullet out of bounds
                relay_messages.append(m)
                self.player_bullets[client_index] = False
                print('Player ' + str(client_index + 1) + ' bullet went out of bounds.')
            elif m[0] == 'b': # Player bullet hit base
                relay_messages.append(m)
                self.player_bullets[client_index] = False
                print('Player ' + str(client_index + 1) + ' bullet hit base ' + m[1:] + '.')
            elif m[0] == 'e': # Own enemy hit
                enemy_id = int(m[1:])
                if self.player_bullets[client_index] and self.remaining_enemies[enemy_id]: # If bullet still exists and enemy is still alive
                    self.player_bullets[client_index] = False
                    self.remaining_enemies[enemy_id] = False
                    self.killed_enemies += 1
                    self.player_score[client_index] += SCORE_INCREMENT
                    return_messages.append('w' + str(enemy_id))
                    relay_messages.append('t' + str(enemy_id))
                    print('Player ' + str(client_index + 1) + ' hit enemy ' + m[1:] + '.')
            elif m == 'p': # Own player hit
                if self.enemy_bullet: # If enemy bullet still exists
                    self.enemy_bullet = False
                    return_messages.append('p')
                    relay_messages.append('o')
                    print('Player ' + str(client_index + 1) + ' got hit.')
            elif m == 'd': # Enemy bullet destroyed
                self.enemy_bullet = False
                print('Enemy bullet destroyed.')
            elif m[0] == 'g': # Notification of game end
                pair = m[1:].split(':')
                self.player_score[0] = int(pair[0])
                self.player_score[1] = int(pair[1])
                self.end_game()
                break # Don't need to process any more messages after game ends
            else:
                print("Error: received in-game message " + m)
    
    # Parses messages if the game is not in progress.
    def parse_outofgame(self, client_index, raw_message):
        response = ''
        if len(raw_message) == 0: # Empty messages of trailing ;
            pass
        elif raw_message == 'l': # Request for leaderboard
            leaderboard = get_leaderboard()
            if len(leaderboard) == 0:
                response = 'n' # 'Null response' if the leaderboard is empty.
            for entry in leaderboard: # Encode entries in leaderboard into a single string to send.
                response += '/' + entry['name']
                response += '$' + str(entry['score'])
        elif raw_message[0] == 'r': # Notification of readiness
            self.player_ready[client_index] = True
            self.player_name[client_index] = raw_message[1:]
            print('Player ' + str(client_index + 1) + ' is ready, name: ' + self.player_name[client_index])
        else:
            print("Error: received out-of-game message " + raw_message)
            # Note that there is a delay between one player claiming the end of the game and the other player
            # receiving the notification that led to that event. Therefore, there will be some residual in-game
            # messages from the other player.
        return response
    
    # Update variables that track time when the game is running.
    def update_time(self):
        time_delta = time.time() - self.game_time
        self.game_time = time.time()
        self.elapsed_time += time_delta
        self.time_since_bullet += time_delta

    # Check to see if we can create an enemy bullet, and if so, choose a random enemy to fire.
    # At the moment the interval for firing is fixed, but we could change this to a random interval if desired.
    def create_enemy_bullet(self):
        if self.time_since_bullet >= ENEMY_BULLET_INTERVAL and not self.enemy_bullet:
            # Only create a new enemy bullet if one does not already exist.
            self.time_since_bullet = 0
            enemy_id = random.randint(0, NUM_ENEMIES - 1)
            while not self.remaining_enemies[enemy_id]: # Keep generating random numbers until we get one
                                                        # that corresponds to a living enemy.
                enemy_id = random.randint(0, NUM_ENEMIES - 1)
            self.enemy_bullet = True
            print('Created bullet at enemy ' + str(enemy_id) + '.')
            return 'e' + str(enemy_id)
        else:
            return ''
    
    # Main update loop of server-side game logic.
    # Arguments: raw TCP/UDP messages from clients.
    # Returns: messages to send back to clients (in same order).
    def update(self, raw_message1, raw_message2):

        if raw_message1 != '' or raw_message2 != '':
            print('Received: 1 = ' + raw_message1 + ' 2 = ' + raw_message2)

        response1, response2 = '', ''

        if self.game_in_progress:
            
            ## Process messages from clients and take direct action
            arr1, arr2 = [], []
            self.parse_ingame(0, raw_message1, arr1, arr2)

            if self.game_in_progress: # Check again since parsing messages may have ended the game

                self.parse_ingame(1, raw_message2, arr2, arr1)

                ## Update time
                self.update_time()

                ## See if we are on a new wave of enemies
                if self.killed_enemies == NUM_ENEMIES:
                    self.killed_enemies = 0
                    for i in range(NUM_ENEMIES):
                        self.remaining_enemies[i] = True

                ## Check if we can create a new enemy projectile
                enemy_bullet_message = self.create_enemy_bullet()
                if enemy_bullet_message != '':
                    arr1.append(enemy_bullet_message)
                    arr2.append(enemy_bullet_message)

            # Join messages from array together into a single string to send.
            if len(arr1) != 0:
                response1 = ';'.join(str(x) for x in arr1) + ';'
            if len(arr2) != 0:
                response2 = ';'.join(str(x) for x in arr2) + ';'

        else:

            ## Check for notifications of readiness and leaderboard requests
            response1 = self.parse_outofgame(0, raw_message1)
            response2 = self.parse_outofgame(1, raw_message2)

            ## Check if both players are ready so we can start the game.
            ## Note that we are assuming that notifications of readiness and requests for
            ## the leaderboard are mutually exclusive.
            if self.player_ready[0] and self.player_ready[1]:
                self.start_game()
                response1 = 's' + self.player_name[1]
                response2 = 's' + self.player_name[0]
        
        # Do not send an empty string.
        if response1 != '' or response2 != '':
            print('Sent: 1 = ' + response1 + ' 2 = ' + response2)

        return response1, response2