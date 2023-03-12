NUM_ENEMIES = 55
SCORE_INCREMENT = 10 # How much a player's score should increase by upon killing an enemy.

class GameServer:

    def reset_game_state(self):
        self.player_ready = [False, False]
        self.player_name = ['', '']
        self.player_score = [0, 0]
        self.game_in_progress = False
        self.remaining_enemies = []
        for i in range(NUM_ENEMIES):
            self.remaining_enemies.append(True) # All enemies are alive at start
        self.bullet_ids = []

    def __init__(self):
        self.reset_game_state()
    
    def end_game(self):
        # Store names and scores of players in leaderboard via DynamoDB
        self.reset_game_state()
    
    def parse_messages(self, client_index, raw_message):
        return_messages = [] # Messages to return to the client that send the incoming message
        relay_messages = [] # Messages to relay to the other client

        messages = raw_message.split(';')
        for m in messages:
            if len(m) == 0: # Empty messages or trailing ;
                pass
            elif not self.game_in_progress and m[0] == 'r': # Notification of readiness
                self.player_ready[client_index] = True
                self.player_name[client_index] = m[1:]
            elif not self.game_in_progress:
                continue # Skip over other messages if game is not in progress
            elif m[0].isdigit(): # Player position
                relay_messages.append(m)
            elif m[0] == 'c': # Player bullet creation
                self.bullet_ids.append(int(m[1:]))
                relay_messages.append(m)
            elif m[0] == 'b': # Bullet-enemy collision
                enemy_id = m[1:].split('e')[1]
                if self.remaining_enemies[enemy_id]: # If collision is valid
                    self.remaining_enemies[enemy_id] = False
                    return_messages.append(m)
                    relay_messages.append(m)
            elif m[0] == 'p': # Player-bullet collision
                bullet_id = m[3:]
                if self.bullet_ids.count(bullet_id) > 0:
                    self.bullet_ids.remove(bullet_id)
                    self.player_score[client_index] += SCORE_INCREMENT
                    return_messages.append(m)
                    relay_messages.append(m)
            elif m[0] == 'g': # Notification of game end
                self.end_game()

        return return_messages, relay_messages

    def format_responses(self, messages):
        f_message = ''
        for m in messages:
            f_message += m + ';'
        return f_message
    
    def update(self, raw_message1, raw_message2): # Raw messages from client 1 and 2

        ## Process messages from clients and take direct action
        response1, response2, temp1, temp2 = [], [], [], []
        response1, response2 = self.parse_messages(0, raw_message1)
        temp1, temp2 = self.parse_messages(1, raw_message2)
        response1 += temp2
        response2 += temp1

        ## Check if both players are ready so we can start the game
        if self.player_ready[0] and self.player_ready[1]:
            self.game_in_progress = True
            response1.append('s')
            response2.append('s')

        

        return self.format_responses(response1), self.format_responses(response2)