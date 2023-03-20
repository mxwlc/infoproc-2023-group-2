import time
import random

from game_server_logic.leaderboard_functions import *
from game_server_logic.create_leaderboard import *

class GameServer:

    def reset_game_state(self):
        self.player_ready = [False, False]
        self.player_name = ['', '']
        self.player_score = [0, 0]
        self.game_in_progress = False
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

    def init_clients(self, public_ips, private_ips):
        self.public_ips = public_ips
        self.private_ips = private_ips

    def start_game(self):
        self.game_in_progress = True
        self.game_time = time.time()
        self.elapsed_time = 0
        print('Started game.')
    
    def end_game(self):
        for i in range(2):
            update_leaderboard(self.player_name[i], self.player_score[i])
        self.reset_game_state()
        print('Ended game.')
    
    # Parses messages if the game is in progress.
    def parse_ingame(self, client_index, m):
        if len(m) == 0: # Empty messages or trailing ;
            pass
        elif m[0] == 'g': # Notification of game end
            pair = m[1:].split(':')
            self.player_score[0] = int(pair[0])
            self.player_score[1] = int(pair[1])
            self.end_game()
        else:
            print("Error: received in-game message " + m)
    
    # Parses messages if the game is not in progress.
    def parse_outofgame(self, client_index, raw_message):
        response = ''
        if len(raw_message) == 0: # Empty messages of trailing ;
            pass
        elif raw_message == 'l': # Request for leaderboard
            leaderboard = get_leaderboard()
            for entry in leaderboard:
                response += '/' + entry['name']
                response += '$' + str(entry['score'])
        elif raw_message[0] == 'r': # Notification of readiness
            self.player_ready[client_index] = True
            self.player_name[client_index] = raw_message[1:]
        else:
            print("Error: received out-of-game message " + raw_message)
            # Note that there is a delay between one player claiming the end of the game and the other player
            # receiving the notification that led to that event. Therefore, there will be some residual in-game
            # messages from the other player.
        return response
    
    # # Update variables that track time when the game is running.
    # def update_time(self):
    #     time_delta = time.time() - self.game_time
    #     self.game_time = time.time()
    #     self.elapsed_time += time_delta
    #     self.time_since_bullet += time_delta

    # # Check to see if we can create an enemy bullet, and if so, choose a random enemy to fire.
    # # At the moment the interval for firing is fixed, but we could change this to a random interval if desired.
    # def create_enemy_bullet(self):
    #     if self.time_since_bullet >= ENEMY_BULLET_INTERVAL and not self.enemy_bullet:
    #         # Only create a new enemy bullet if one does not already exist.
    #         self.time_since_bullet = 0
    #         enemy_id = random.randint(0, NUM_ENEMIES - 1)
    #         while not self.remaining_enemies[enemy_id]:
    #             enemy_id = random.randint(0, NUM_ENEMIES - 1)
    #         self.enemy_bullet = True
    #         return 'e' + str(enemy_id)
    #     else:
    #         return ''
    
    # Main update loop of server-side game logic.
    # Arguments: raw TCP/UDP messages from clients.
    # Returns: messages to send back to clients (in same order).
    def update(self, raw_message1, raw_message2):

        if raw_message1 != '' or raw_message2 != '':
            print('Received: 1 = ' + raw_message1 + ' 2 = ' + raw_message2)

        response1, response2 = '', ''

        if self.game_in_progress:
            
            self.parse_ingame(0, raw_message1)

            if self.game_in_progress: # Game may have ended
                self.parse_ingame(1, raw_message2)

        else:

            ## Check for notifications of readiness and leaderboard requests
            response1 = self.parse_outofgame(0, raw_message1)
            response2 = self.parse_outofgame(1, raw_message2)

            ## Check if both players are ready so we can start the game.
            ## Note that we are assuming that notifications of readiness and requests for
            ## the leaderboard are mutually exclusive.
            if self.player_ready[0] and self.player_ready[1]:
                self.start_game()
                response1 = 'sl' + self.player_name[1]
                response2 = 'sc' + self.player_name[0] + ':' + self.public_ips[0] + ':' + self.private_ips[0]
        
        if response1 != '' or response2 != '':
            print('Sent: 1 = ' + response1 + ' 2 = ' + response2)

        return response1, response2