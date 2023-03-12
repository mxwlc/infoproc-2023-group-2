import time
import random

from leaderboard_functions import *
from create_leaderboard import *

NUM_ENEMIES = 55
SCORE_INCREMENT = 10 # How much a player's score should increase by upon killing an enemy.
ENEMY_BULLET_INTERVAL = 2 # Time in seconds between spawnings of enemy bullets.

class GameServer:

    def reset_game_state(self):
        self.player_ready = [False, False]
        self.player_name = ['', '']
        self.player_score = [0, 0]
        self.game_in_progress = False
        self.remaining_enemies = []
        for i in range(NUM_ENEMIES):
            self.remaining_enemies.append(True)
        self.bullet_ids = []

    def __init__(self):
        try:
            create_leaderboard()
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
    
    def end_game(self):
        for i in range(2):
            update_leaderboard(self.player_name[i], self.player_score[i])
        self.reset_game_state()
    
    # Parses messages if the game is in progress.
    # Return messages: messages to return to the client that sent the incoming (raw) message.
    # Relay messages: messages to relay to the other client.
    def parse_ingame(self, client_index, raw_message, return_messages, relay_messages):
        messages = raw_message.split(';')
        for m in messages:
            if len(m) == 0: # Empty messages or trailing ;
                pass
            elif m[0].isdigit(): # Player position
                relay_messages.append(m)
            elif m[0] == 'c': # Player bullet creation
                self.bullet_ids.append(int(m[1:]))
                relay_messages.append(m)
            elif m[0] == 'b': # Bullet-enemy collision
                enemy_id = m[1:].split('e')[1]
                if self.remaining_enemies[enemy_id]: # If collision is valid
                    self.remaining_enemies[enemy_id] = False
                    self.player_score[client_index] += SCORE_INCREMENT
                    return_messages.append(m)
                    relay_messages.append(m)
            elif m[0] == 'p': # Player-bullet collision
                bullet_id = m[3:]
                if self.bullet_ids.count(bullet_id) > 0:
                    self.bullet_ids.remove(bullet_id)
                    return_messages.append(m)
                    relay_messages.append(m)
            elif m[0] == 'g': # Notification of game end
                self.end_game()
    
    # Parses messages if the game is not in progress.
    def parse_outofgame(self, client_index, raw_message):
        response = ''
        if raw_message[0] == 'r': # Notification of readiness
            self.player_ready[client_index] = True
            self.player_name[client_index] = raw_message[1:]
        elif raw_message == 'l': # Request for leaderboard
            leaderboard = get_leaderboard()
            for entry in leaderboard:
                response += 'n' + entry['name']
                response += 's' + entry['score']
        
        return response

    # Convert a list of messages into a single message separated by ';'.
    def format_responses(self, messages):
        f_message = ''
        for m in messages:
            f_message += m + ';'
        return f_message
    
    # Update variables that track time when the game is running.
    def update_time(self):
        time_delta = time.time() - self.game_time
        self.game_time = time.time()
        self.elapsed_time += time_delta
        self.time_since_bullet += time_delta

    # Check to see if we can create an enemy bullet, and if so, choose a random enemy to fire.
    # At the moment the interval for firing is fixed, but we could change this to a random interval if desired.
    def create_enemy_bullet(self):
        if self.time_since_bullet >= ENEMY_BULLET_INTERVAL:
            self.time_since_bullet = 0
            enemy_id = random.randint(0, NUM_ENEMIES - 1)
            return 'e' + str(enemy_id)
        else:
            return ''
    
    # Main update loop of server-side game logic.
    # Arguments: raw TCP/UDP messages from clients.
    # Returns: messages to send back to clients (in same order).
    def update(self, raw_message1, raw_message2):

        response1, response2 = '', ''

        if self.game_in_progress:
            
            ## Process messages from clients and take direct action
            arr1, arr2 = [], []
            self.parse_ingame(0, raw_message1, arr1, arr2)
            self.parse_ingame(1, raw_message2, arr2, arr1)

            if self.game_in_progress: # Check again since parsing messages may have ended the game

                ## Update time
                self.update_time()

                ## Check if we can create a new enemy projectile
                enemy_bullet_message = self.create_enemy_bullet()
                arr1.append(enemy_bullet_message) # This message may be empty
                arr2.append(enemy_bullet_message)

            response1 = self.format_responses(arr1)
            response2 = self.format_responses(arr2)

        else:

            ## Check for notifications of readiness and leaderboard requests
            response1 = self.parse_outofgame(0, raw_message1)
            response2 = self.parse_outofgame(1, raw_message2)

            ## Check if both players are ready so we can start the game.
            ## Note that we are assuming that notifications of readiness and requests for
            ## the leaderboard are mutually exclusive.
            if self.player_ready[0] and self.player_ready[1]:
                self.start_game()
                response1 = 's'
                response2 = 's'

        return response1, response2