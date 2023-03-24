# Import this class into server.py to execute the server-side game logic.
# After instantiating the class, the only method needed to interface with it is update.

import time
import random
import json

# Import leaderboard interface.
from game_server_logic.leaderboard_functions import *
from game_server_logic.create_leaderboard import *

# Import recovery save interface.
from game_server_logic.recovery_functions import *

# Import Decimal to int encoder.
from game_server_logic.decimal_encoder import *

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
    
    # Create a new recovery save in the database with the given game state data.
    def parse_ingame_exit(self, message, ips):
        identifier = [[ips[0], self.player_name[0]], [ips[1], self.player_name[1]]]
        game_state = json.loads(message[1:])
        new_recovery(str(identifier), game_state)
        print('Created new recovery save with identifier ' + str(identifier) + '.')
    
    # Parses messages if the game is in progress.
    # Return messages: messages to return to the client that sent the incoming (raw) message.
    # Relay messages: messages to relay to the other client.
    def parse_ingame(self, client_index, raw_message, responses, ips):
        return_messages = responses[client_index]
        relay_messages = responses[1 - client_index]
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
            elif m == 'd': # Enemy bullet out of bounds
                self.enemy_bullet = False
                print('Enemy bullet went out of bounds.')
            elif m[0] == 'g': # Notification of game end
                pair = m[1:].split(':')
                for i in range(2):
                    self.player_score[i] = int(pair[i])
                self.end_game()
                break # Don't need to process any more messages after game ends
            elif m[0] == 'z': # Notification of in-game exit
                self.parse_ingame_exit(m, ips)
                relay_messages.append('x')
                self.reset_game_state()
                return True
            elif m == 'x': # Notification of out-of-game exit
                break
            else:
                print("Error: received in-game message " + m + '.')
        return False
    
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
        elif raw_message == 'x': # Client exit
            pass
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
    
    # Loads a game from a recovery save.
    # Returns the messages for client 1 and 2.
    def load_from_save(self, recovery_db_response):
        game_state = recovery_db_response['game_state']
        i = 1 if self.player_name[1] == game_state['player_name'][0] else 0
            # 1 if player 1 and player 2 are swapped in the game state record, 0 otherwise
        self.player_bullets[i] = game_state['player_bullet_y'][0] != 500
        self.player_bullets[1 - i] = game_state['player_bullet_y'][1] != 500
        for i in range(NUM_ENEMIES):
            if game_state['enemy_yvel'][i] == 0:
                self.killed_enemies += 1
                self.remaining_enemies[i] = False
        self.enemy_bullet = game_state['enemy_bullet_y'] != 1000
        return 'z' + json.dumps(game_state, separators=(',', ':'), cls=DecimalEncoder)

    # Main update loop of server-side game logic.
    # Arguments: raw TCP/UDP messages from clients.
    # Returns: messages to send back to clients (in same order).
    def update(self, raw_message, ips):

        if raw_message[0] != '' or raw_message[1] != '':
            print('Received: 1 = ' + raw_message[0] + ' 2 = ' + raw_message[1])

        response = ['', '']
        crash_game = False

        if self.game_in_progress:
            
            temp_arr = [[], []]

            for i in range(2):
                crash_game = self.parse_ingame(i, raw_message[i], temp_arr, ips)
                if not self.game_in_progress:
                    break # Don't need to parse any more.
            
            if self.game_in_progress: # Check if game is still in progress after parsing messages.

                # Update time.
                self.update_time()

                # See if we are on a new wave of enemies.
                if self.killed_enemies == NUM_ENEMIES:
                    self.killed_enemies = 0
                    for i in range(NUM_ENEMIES):
                        self.remaining_enemies[i] = True

                # Check if we can create a new enemy projectile.
                enemy_bullet_message = self.create_enemy_bullet()
                if enemy_bullet_message != '':
                    for i in range(2):
                        temp_arr[i].append(enemy_bullet_message)

            # Join messages from array together into a single string to send.
            for i in range(2):
                if len(temp_arr[i]) != 0:
                    response[i] = ';'.join(str(x) for x in temp_arr[i]) + ';'

        else:

            # Check for notifications of readiness and leaderboard requests.
            for i in range(2):
                response[i] = self.parse_outofgame(i, raw_message[i])

            # Check if both players are ready so we can start the game.
            # Note that notifications of readiness and requests for the leaderboard are mutually exclusive.
            if self.player_ready[0] and self.player_ready[1]:
                self.start_game()
                pair1 = [ips[0], self.player_name[0]]
                pair2 = [ips[1], self.player_name[1]]
                id1 = [pair1, pair2]
                id2 = [pair2, pair1]
                recovery_db_response = get_recovery(str(id1))
                if recovery_db_response == None:
                    recovery_db_response = get_recovery(str(id2))
                # get_recovery(str(id1)) and get_recovery(str(id2)) cannot both be non-null since this would imply
                # two identical entries in the recovery database, just with the identifiers swapped,
                # which is not possible because entries are deleted when accessed.
                
                # If there is a recovery save, load from that, otherwise start a fresh game.
                if recovery_db_response != None:
                    response[0] = response[1] = self.load_from_save(recovery_db_response)
                else:
                    for i in range(2):
                        response[i] = 's' + self.player_name[1 - i]
        
        if response[0] != '' or response[1] != '':
            print('Sent: 1 = ' + response[0] + ' 2 = ' + response[1])

        return response, crash_game