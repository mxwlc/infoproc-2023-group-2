import pygame
import random
import math
import sys
import os
#import host
from button import Button
import atexit

from tcp_client import *

SCORE_INCREMENT = 10

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
menu_bg = pygame.image.load(os.path.join("assets", "menu_bg.png"))
pygame.display.set_caption("Menu")
icon = pygame.image.load(os.path.join("assets", "icon.png"))
pygame.display.set_icon(icon)
font = pygame.font.SysFont('arialblack', 35)  # fonts
fontl = pygame.font.SysFont('cambria', 64)
fonts = pygame.font.SysFont('arialblack', 20)
fontss = pygame.font.SysFont('arialblack', 15)
over_font = pygame.font.SysFont('arialblack', 72)
text_colour = (255, 255, 255)  # colours
colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('gray15')
colour_gold = '#b68f40'
#fpga = host.FPGAController()

tcp_client = TCPClient()
tcp_client.connect_to_server()

def exit_handler():
    tcp_client.send_server('x')
    tcp_client.send_peer('x')
    tcp_client.close()

atexit.register(exit_handler)


class Bunker:
    def __init__(self, X, Y, Health):
        self.X = X
        self.Y = Y
        self.Health = Health

    def draw(self):
        image = pygame.image.load(os.path.join("assets", "bunker.png"))
        screen.blit(image, (self.X, self.Y))

    def lose_health(self):
        self.Health -= 1
        if self.Health == 0:
            self.X = -50


class Player:
    def __init__(self, X, Y, Lives, Score, Bullet_State, bulletImg):
        self.X = X
        self.Y = Y
        self.Lives = Lives
        self.Score = Score
        self.Bullet_State = Bullet_State
        self.bulletImg = bulletImg

    def draw(self, image):
        screen.blit(image, (self.X, self.Y))

    def add_score(self, bonus):
        self.Score += bonus

    def lose_lives(self):
        self.Lives -= 1

    def shoot(self, X, Y):
        self.Bullet_State = "fire"
        screen.blit(bulletImg, (X + 16, Y + 10))


# enemy grid
enemyImg = []
enemyX_change = []
enemyY_change = []
enemyX = [50]
enemyY = [50]
num_of_enemies = 44

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join("assets", "enemy.png")))

# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load(os.path.join("assets", "player_bullet.png"))
bulletY_change = 5 #bullet speed
player1_bulletX = 0  # player1 bullet
player1_bulletY = 500
player2_bulletX = 0  # player2 bullet
player2_bulletY = 500
enemy_bulletImg = pygame.image.load(os.path.join("assets", "enemy_bullet.png"))  # enemy bullet
enemy_bulletX = 0
enemy_bulletY = 500
enemy_bulletY_change = 5 #bullet speed
enemy_bullet_state = "ready"

# Player1
player1_name = 'Player1'
player1Img = pygame.image.load(os.path.join("assets", "player.png"))
player1X_change = 0 
Player1 = Player(300, 500, 5, 0, "ready", bulletImg)
score_value1 = Player1.Score  # player 1 score
live_value1 = Player1.Lives

# Player2/remote player
player2_name = 'Player2'
player2Img = pygame.image.load(os.path.join("assets", "player2.png"))
player2X_change = 0
Player2 = Player(500, 500, 5, 0, "ready", bulletImg)
score_value2 = Player2.Score
live_value2 = Player2.Lives

# velocity
player_vel = 2
enemy_vel = 1

# bunker
bunker_health = 4
bunker_width = pygame.image.load(os.path.join("assets", "bunker.png")).get_width()
space = (width - 80 - bunker_width * 4) / 3 + bunker_width
bunkers = []
for i in range(4):
    bunkers.append(Bunker(40 + space * i, 450, bunker_health))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit means to draw


def isCollision(X1, Y1, X2, Y2):
    distance = math.sqrt(math.pow(X1 - X2, 2) + math.pow(Y1 - Y2, 2))
    if distance < 25:
        return True
    else:
        return False


def enemy_attack(x, y): #when this is called, enemy_bulletY changes so bullet is moving down  
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletImg, (x + 16, y + 10))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def show_my_score(score_value1):
    score = fonts.render("Player " + player1_name + " Score :" + str(score_value1), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def show_other_score(score_value2):
    score = fonts.render("Player " + player2_name + " Score :" + str(score_value2), True, (255, 255, 255))
    screen.blit(score, (10, 30))


def show_live(live_value1):
    life = fonts.render("Player " + player1_name + " Lives :" + str(live_value1), True, (255, 255, 255))
    screen.blit(life, (550, 10))


def show_other_live(live_value2):
    life = fonts.render("Player " + player2_name + " Lives :" + str(live_value2), True, (255, 255, 255))
    screen.blit(life, (550, 30))


def game_over_screen(I_Won):
    over_text = over_font.render("GAME OVER", True, 'white')
    screen.blit(over_text, (width / 2 - over_text.get_width() / 2, 150))
    win = fonts.render("You Win!", True, 'white')
    lose = fonts.render("You Lose", True, 'white')
    if I_Won:
        screen.blit(win, (width / 2 - win.get_width() / 2, 300))
    else:
        screen.blit(lose, (width / 2 - win.get_width() / 2, 300))


def boundary(X1):
    if X1 <= 0:
        X1 = 0
    elif X1 >= 730:
        X1 = 730
    return X1


unavailable = [] #killed enemies cannot shoot
killed = 0


def LevelUpReset(): #when all enemy killed and game level up, the list of 'dead' and bodycount resets 
    global unavailable, killed
    unavailable.clear()
    killed = 0


def NewGameReset(): #resets all global variables, new game
    global Player1, Player2, bunkers, player1X_change, player2X_change, score_value1, live_value1, score_value2, live_value2, enemy_vel
    global hit_enemy_id, was_hit
    hit_enemy_id = -1
    was_hit = False
    player1X_change = 0
    Player1 = Player(300, 500, 5, 0, "ready", bulletImg)
    score_value1 = Player1.Score
    live_value1 = Player1.Lives
    player2X_change = 0
    Player2 = Player(500, 500, 5, 0, "ready", bulletImg)
    score_value2 = Player2.Score
    live_value2 = Player2.Lives
    enemy_vel = 1
    for i in range(4):
        bunkers[i].X = 40 + space * i
        bunkers[i].Health = bunker_health


def EnemyLevelUp():  # reset positions of enemies
    global enemyX, enemyY, enemy_vel, num_of_enemies, enemyX_change, enemyY_change
    enemyX_change.clear()
    enemyY_change.clear()
    LevelUpReset()
    enemyX = [50]
    enemyY = [50]
    for i in range(num_of_enemies):
        n = i + 1
        if n % 11 == 0:
            enemyX.append(50)
            enemyY.append(enemyY[i - 1] + 50)
        else:
            enemyX.append(enemyX[i] + 50)
            enemyY.append(enemyY[i])
        enemyX_change.append(enemy_vel)
        enemyY_change.append(20)


sync_var = True # A variable used to synchronise events between peers.
turn_to_shoot = True # Whether it's this client's turn to shoot an enemy bullet.
shoot_now = True # Whether we should shoot an enemy bullet now.
shoot_enemy_id = -1 # ID of enemy that should should now.
hit_enemy_id = -1 # ID of enemy that was hit by this player
was_hit = False
rtt = 0 # Round trip time between peers.
frame_delay = 0 # rtt -> frame delay
fps = 60

def parse_peer(responses):
    messages = tcp_client.recv_peer().split(';')
    global player1X_change, player2X_change, enemy_bullet_state, player1_bulletX, player2_bulletX, enemy_bulletX, enemy_bulletY, player1_bulletY, player2_bulletY, killed, unavailable, enemy_vel
    global sync_var, hit_enemy_id, was_hit, turn_to_shoot
    for m in messages: # TODO consider iterating backwards through messages
        if len(m) == 0: # Empty messages or trailing ;
            pass
        elif m[0].isdigit(): # Other player position
            Player2.X = int(m)
        elif m == 'c': # Other player bullet creation
            player2_bulletX = Player2.X
            Player2.shoot(player2_bulletX, player2_bulletY)
            print('Other player shot bullet.')
        elif m[0] == 'e': # Enemy creates bullet
            enemy_id = int(m[1:])
            enemy_bulletX = enemyX[enemy_id]
            enemy_bulletY = enemyY[enemy_id]
            enemy_attack(enemy_bulletX, enemy_bulletY)
            turn_to_shoot = True
            print('From other client: enemy ' + str(enemy_id) + ' shot bullet.')
        elif m[0] == 'b': # Registered collision between enemy and player bullet
            enemy_id = int(m[1:])
            if enemy_id == hit_enemy_id:
                if sync_var: # Own player hits enemy with bullet
                    player1_bulletY = 500
                    Player1.Bullet_State = "ready"
                    Player1.add_score(SCORE_INCREMENT)
                    enemy_id = int(m[1:])
                    enemyX[enemy_id] = 1000
                    enemyY[enemy_id] = -1000
                    unavailable.append(enemy_id)
                    killed += 1
                    print('Decided: own player hit enemy.')
                else: # Other player hits enemy with bullet
                    player2_bulletY = 500
                    Player2.Bullet_State = "ready"
                    Player2.add_score(SCORE_INCREMENT)
                    enemy_id = int(m[1:])
                    enemyX[enemy_id] = 1000
                    enemyY[enemy_id] = -1000
                    unavailable.append(enemy_id)
                    killed += 1
                    print('Decided: other player hit enemy.')
                sync_var = not sync_var
            else:
                player2_bulletY = 500
                Player2.Bullet_State = "ready"
                Player2.add_score(SCORE_INCREMENT)
                enemy_id = int(m[1:])
                enemyX[enemy_id] = 1000
                enemyY[enemy_id] = -1000
                unavailable.append(enemy_id)
                killed += 1
                responses.append('w')
                print('Other player hit enemy.')
        elif m == 'w': # Own player hits enemy with bullet
            player1_bulletY = 500
            Player1.Bullet_State = "ready"
            Player1.add_score(SCORE_INCREMENT)
            enemyX[hit_enemy_id] = 1000
            enemyY[hit_enemy_id] = -1000
            unavailable.append(hit_enemy_id)
            killed += 1
            print('Own player hit enemy.')
        elif m == 'p': # Register collision between player and enemy bullet
            if was_hit:
                if sync_var: # Own player hit
                    enemy_bulletY = 1000
                    Player1.lose_lives()
                    print('Decided: own player got hit.')
                else: # Other player hit
                    enemy_bulletY = 1000
                    Player2.lose_lives()
                    print('Decided: other player got hit.')
                was_hit = False
                sync_var = not sync_var
            else:
                enemy_bulletY = 1000
                Player2.lose_lives()
                responses.append('h')
                print('Other player got hit.')
        elif m == 'h': # Own player gets hit with enemy bullet
            enemy_bulletY = 1000
            Player1.lose_lives()
            was_hit = False
            print('Own player got hit.')
        else:
            print("Error: received message " + m)

def return_peer(responses):
    if len(responses) != 0:
        tcp_client.send_peer(';'.join(str(x) for x in responses) + ';')

def play():  # Todo: 1.change input method to FPGA input  2.send data to server
    pygame.display.set_caption('Space Invaders')
    # add fps to synchronise the game on different devices
    clock = pygame.time.Clock()
    NewGameReset()
    EnemyLevelUp()
    # Game Loop
    global player1X_change, player2X_change, enemy_bullet_state, player1_bulletX, player2_bulletX, enemy_bulletX, enemy_bulletY, player1_bulletY, player2_bulletY, killed, unavailable, enemy_vel
    global hit_enemy_id, was_hit, sync_var, turn_to_shoot, shoot_now, shoot_enemy_id, fps, rtt, frame_delay
    running = True
    over = False
    I_Won = False
    enemy_shoot_counter = 0

    while running:
        # RGB Red, Green, Blue color
        screen.fill((0, 0, 0))
        #screen.blit(menu_bg, (0, 0))

        peer_responses = []

        # Handle incoming messages
        parse_peer(peer_responses)

        for event in pygame.event.get():  # check all the events in the window
            if event.type == pygame.QUIT:
                running = False
                start_menu()
            # # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1X_change = -player_vel
                if event.key == pygame.K_RIGHT:
                    player1X_change = player_vel
                if event.key == pygame.K_DOWN: # Kill button
                    Player1.Lives = 0
                # if event.key == pygame.K_a:
                #     player2X_change = -player_vel
                # if event.key == pygame.K_d:
                #     player2X_change = player_vel
                if event.key == pygame.K_SPACE:
                    if Player1.Bullet_State == "ready":
                        player1_bulletX = Player1.X
                        Player1.shoot(player1_bulletX, player1_bulletY)
                        peer_responses.append('c')
                        print('Shot bullet.')
                # if event.key == pygame.K_TAB:
                #     if Player2.Bullet_State == "ready":
                #         player2_bulletX = Player2.X
                #         Player2.shoot(player2_bulletX, player2_bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1X_change = 0
                # if event.key == pygame.K_a or event.key == pygame.K_d:
                #     player2X_change = 0

        # checking for boundaries of spaceship sp it doesn't go out of bounds
        Player1.X += player1X_change
        # Player2.X += player2X_change
        Player1.X = boundary(Player1.X)
        # Player2.X = boundary(Player2.X)

        peer_responses.append(str(Player1.X))

        # Delay enemy shooting by one cycle to help with synchronisation
        # + number in frame_delay (due to RTT)
        if shoot_now:
            if enemy_shoot_counter < frame_delay:
                enemy_shoot_counter += 1
            else:
                print('Shoot from enemy ' + str(shoot_enemy_id) + '.')
                enemy_bulletX = enemyX[shoot_enemy_id]
                enemy_bulletY = enemyY[shoot_enemy_id]
                enemy_attack(enemy_bulletX, enemy_bulletY)
                shoot_now = False
                enemy_shoot_counter = 0
        
        # Choose random enemy to shoot
        if random.randint(0, 100) < 10 and turn_to_shoot and enemy_bullet_state == 'ready':
            shoot_now = True
            turn_to_shoot = False
            shoot_enemy_id = random.randint(0, 43)
            while shoot_enemy_id in unavailable:
                shoot_enemy_id = random.randint(0, 43)  # the enemy corresponfing to that number will shoot
            peer_responses.append('e' + str(shoot_enemy_id))
                
        
        # enemy movement
        for i in range(num_of_enemies):
            # game over logic 
            if enemyY[i] > 400: #when enemy reaches bottom
                Player1.Lives = 0
                Player2.Lives = 0
                over = True
                I_Won = (score_value1 > score_value2)

            if Player1.Lives == 0 and Player1.Lives < Player2.Lives: 
                I_Won = False
                over = True
            elif Player2.Lives == 0 and Player1.Lives > Player2.Lives:
                I_Won = True
                over = True
            if over:
                # for j in range(num_of_enemies):
                #     enemyY[j] = -2000
                print('Game ended.')
                tcp_client.send_server('g' + str(Player1.Score) + ':' + str(Player2.Score)) # End game immediately
                return_peer(peer_responses) # Flush all remaining peer repsonses

                game_over_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - game_over_time < 3000: #display game over for 3 seconds
                    # Render the game over text
                    game_over_screen(I_Won) #display game over and whether you lost/won
                    pygame.display.update()
                running = False
                leaderboard()

            if enemyX[i] == 1000: #when an enemy is killed, its x position sets to 1000(removed from screen)
                enemyX_change[i] = 0 #cannot move
                enemyY_change[i] = 0

            enemyX[i] += enemyX_change[i] #moves horizontally

            if enemyX[i] <= 20: #when at the edge of screen, go down a row and reverse direction
                enemyX_change[i] = enemy_vel
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 730:
                enemyX_change[i] = -enemy_vel
                enemyY[i] += enemyY_change[i]

            # collision detection
            if isCollision(enemyX[i], enemyY[i], player1_bulletX, player1_bulletY) and i != hit_enemy_id: #for player1
                peer_responses.append('b' + str(i))
                hit_enemy_id = i
                print('Detected: player hit enemy.')
            # if isCollision(enemyX[i], enemyY[i], player2_bulletX, player2_bulletY): #for player2

            if killed == num_of_enemies:
                EnemyLevelUp()
                enemy_vel += 1

        for i in range(4):
            if isCollision(bunkers[i].X, bunkers[i].Y, enemy_bulletX, enemy_bulletY):
                bunkers[i].lose_health()
                enemy_bulletY = 1000
                # remove bunker from screen

        # player1_bullet movement

        if player1_bulletY <= -5: #when bullet out of scope, player can shoot again
            player1_bulletY = 500
            Player1.Bullet_State = "ready"

        if Player1.Bullet_State == "fire": 
            Player1.shoot(player1_bulletX, player1_bulletY)
            player1_bulletY -= bulletY_change

        if player2_bulletY <= -5:
            player2_bulletY = 500
            Player2.Bullet_State = "ready"

        if Player2.Bullet_State == "fire":
            Player2.shoot(player2_bulletX, player2_bulletY)
            player2_bulletY -= bulletY_change

        # enemy bullet movement
        if enemy_bulletY >= 610 and enemy_bulletY != 1000:
            enemy_bulletY = 1000
            enemy_bullet_state = "ready"

        if enemy_bullet_state == "fire":
            enemy_attack(enemy_bulletX, enemy_bulletY)
            enemy_bulletY += enemy_bulletY_change

        if isCollision(Player1.X, Player1.Y, enemy_bulletX, enemy_bulletY) and not was_hit:
            peer_responses.append('p')
            was_hit = True
        # if isCollision(Player2.X, Player2.Y, enemy_bulletX, enemy_bulletY):

        Player1.draw(player1Img)  # draw player1
        Player2.draw(player2Img)  # draw player2
        for i in range(num_of_enemies): #draw enemies
            enemy(enemyX[i], enemyY[i], i)
        for bunker in bunkers: #draw bunkers
            bunker.draw()

        show_my_score(Player1.Score)
        show_other_score(Player2.Score)
        show_live(Player1.Lives)
        show_other_live(Player2.Lives)
        pygame.display.update()
        clock.tick(fps)
        
        return_peer(peer_responses)


# to be modified
def leaderboard():
    pygame.display.set_caption('Leaderboard')

    tcp_client.send_server('l')
    print('Fetching leaderboard...')
    response = ''
    while True:
        response = tcp_client.recv_server()
        if response != '':
            break
    print('Received leaderboard.')
    
    raw_pairs = response.split('/')
    pairs = []
    for pair in raw_pairs:
        if pair == '':
            continue
        pairs.append(pair.split('$'))
    # pairs is an array where each element is a 2-element array representing the name and score of a player.
    # e.g. pairs[0][0] is the first name, and pairs[0][1] is the score for that player.
    for pair in pairs:
        print('Name: ' + pair[0] + ', Score: ' + pair[1])

    while True:
        screen.blit(menu_bg, (0, 0))
        lb_text = font.render("LEADERBOARD", True, colour_gold)
        screen.blit(lb_text, (250, 50))
        return_text = fontss.render("Press 'Enter' to continue", True, (255, 255, 255))
        screen.blit(return_text, (550, 550))

        # Display names and scores on the screen
        for pair in pairs:
            name_text = font.render(pair[0], True, 'white')
            score_text = font.render(pair[1], True, 'white')
            screen.blit(name_text, (200, 150 + (pair*30)))
            screen.blit(score_text, (500, 150 + (pair*30)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_menu()
        pygame.display.update()


def start_menu():  # Todo: change input method to FPGA input
    # use keyboard up and down to navigate; use 'enter' to select
    pygame.display.set_caption('Menu')

    position = [400, 225]  # set initial position

    while True:
        screen.blit(menu_bg, (0, 0))

        menu_text = fontl.render("MAIN MENU", True, colour_gold)
        menu_rect = menu_text.get_rect(center=(400, 100))

        play_button = Button(image=pygame.image.load(os.path.join("assets", "Play Rect.png")), pos=(400, 225),
                             text_input="PLAY", font=font, base_color=colour_gold, hovering_color=colour_active)
        leaderboard_button = Button(image=pygame.image.load(os.path.join("assets", "Leaderboard Rect.png")), pos=(400, 350),
                                    text_input="LEADERBOARD", font=font, base_color=colour_gold, hovering_color=colour_active)
        quit_button = Button(image=pygame.image.load(os.path.join("assets", "Quit Rect.png")), pos=(400, 475),
                             text_input="QUIT", font=font, base_color=colour_gold, hovering_color=colour_active)

        screen.blit(menu_text, menu_rect)

        for button in [play_button, leaderboard_button, quit_button]:
            button.changeColor(position)
            button.update(screen)

        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_event.type == pygame.KEYDOWN:
                if menu_event.key == pygame.K_RETURN:
                    if position[1] == 225:  # select play
                        input_id()
                    if position[1] == 350:  # select leaderboard
                        leaderboard()
                    if position[1] == 475:  # select quit
                        pygame.quit()
                        sys.exit()
                if menu_event.key == pygame.K_UP:
                    if position[1] == 225:
                        position[1] = 225
                    else:
                        position[1] = position[1] - 125
                elif menu_event.key == pygame.K_DOWN:
                    if position[1] == 475:
                        position[1] = 475
                    else:
                        position[1] = position[1] + 125
                for button in [play_button, leaderboard_button, quit_button]:
                    button.changeColor(position)
                    button.update(screen)

        pygame.display.update()


def input_id():
    # Todo: 1.change input method to FPGA input done
    #  2.let each player input their names separately, game can't start until both players have input their names
    # use keyboard up, down, left and right to navigate; use 'enter' to select
    pygame.display.set_caption('Input ID')

    user1_text = ''
    # user2_text = ''
    input_rect1 = pygame.Rect(300, 200, 140, 32)  # (left, top, width, height)
    # input_rect2 = pygame.Rect(300, 300, 140, 32)
    colour = [colour_active, colour_passive]
    position = [400, 210]

    while True:

        # check position
        if position[1] == 210:
            active1 = True
            # active2 = False
        # elif position[1] == 310:
        #     active1 = False
        #     active2 = True
        else:
            active1 = False
            # active1 = active2 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and position[1] != 410:
                    position[1] = position[1] + 200
                elif event.key == pygame.K_UP and position[1] != 210:
                    position[1] = position[1] - 200
                elif event.key == pygame.K_RIGHT and position[0] == 400:
                    position = [700, 500]
                elif event.key == pygame.K_LEFT and position[0] == 700:
                    position = [400, 410]
                elif event.key == pygame.K_RETURN:
                    if position == [400, 410]:
                        global player1_name
                        player1_name = user1_text
                        print('Contacting server to start game...')
                        tcp_client.send_server('r' + player1_name)
                        # For now, assume that player1_name is the name of this client's player.
                        global player2_name
                        response = ''
                        # TODO replace this while loop with a proper waiting screen.
                        while True:
                            response = tcp_client.recv_server()
                            if response != '' and response[0] == 's':
                                print('Response received.')
                                triple = response[2:].split(':')
                                player2_name = triple[0]
                                global sync_var, turn_to_shoot, rtt, frame_delay, fps
                                if response[1] == 'l':
                                    print('Starting game as listener.')
                                    tcp_client.listen_for_peer()
                                    rtt = tcp_client.transmit_RTT()
                                    print('RTT calculated as ' + str(rtt) + ' s.')
                                    sync_var = True
                                    turn_to_shoot = True
                                elif response[1] == 'c':
                                    print('Starting game as connector.')
                                    tcp_client.connect_to_peer(triple[1:])
                                    rtt = tcp_client.receive_RTT()
                                    print('RTT calculated as ' + str(rtt) + ' s.')
                                    sync_var = False
                                    turn_to_shoot = False
                                else:
                                    print('Error: received message ' + response)
                                frame_delay = round(rtt * fps)
                                break
                            else:
                                print('Error: received response' + response)
                        play()
                    if position == [700, 500]:
                        start_menu()
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        user1_text = user1_text[:-1]
                    else:
                        user1_text += event.unicode
                # if active2:
                #     if event.key == pygame.K_BACKSPACE:
                #         user2_text = user2_text[:-1]
                #     else:
                #         user2_text += event.unicode

        screen.blit(menu_bg, (0, 0))

        start_button = Button(image=pygame.image.load(os.path.join("assets", "Start Rect.png")), pos=(400, 400),
                              text_input="START GAME", font=fonts, base_color=colour_gold, hovering_color=colour_active)
        start_button.changeColor(position)
        start_button.update(screen)

        return_button = Button(image=pygame.image.load(os.path.join("assets", "Return Rect.png")), pos=(700, 500),
                               text_input="RETURN", font=fontss, base_color="black", hovering_color=colour_active)
        return_button.changeColor(position)
        return_button.update(screen)

        if active1:
            colour[0] = colour_active
            colour[1] = colour_passive
        # elif active2:
        #     colour[0] = colour_passive
        #     colour[1] = colour_active
        else:
            colour = [colour_passive, colour_passive]

        text1 = fonts.render("Player1 ID:", True, (255, 255, 255))
        screen.blit(text1, (300, 150))
        # text2 = fonts.render("Player2 ID:", True, (255, 255, 255))
        # screen.blit(text2, (300, 250))

        pygame.draw.rect(screen, colour[0], input_rect1, 2)
        # pygame.draw.rect(screen, colour[1], input_rect2, 2)

        text_surface1 = fonts.render(user1_text, True, (255, 255, 255))
        # text_surface2 = fonts.render(user2_text, True, (255, 255, 255))
        screen.blit(text_surface1, (input_rect1.x + 5, input_rect1.y + 5))
        # screen.blit(text_surface2, (input_rect2.x + 5, input_rect2.y + 5))

        input_rect1.w = max(200, text_surface1.get_width() + 10)
        # input_rect2.w = max(200, text_surface2.get_width() + 10)

        #fpga.update_hex(player1_name)
        pygame.display.flip()


start_menu()
