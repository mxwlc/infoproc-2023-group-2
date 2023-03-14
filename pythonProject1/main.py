import pygame
import random
import math

# Initialize the pygame
pygame.init()

# create the screen, x-axis:800, y-axis:600
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# background
# background = pygame.image.load('background.png')

# Caption and Ican
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


# Bunker
bunkerImg = []
BunkerX = [20]
BunkerY = [400]
num_of_bunker = 4

for i in range(num_of_bunker):
    n = i + 1
    bunkerImg.append(pygame.image.load('bunker.png'))   
    BunkerX.append(BunkerX[i] + 240)
    BunkerY.append(BunkerY[i])

# Enemy
enemyImg = []
enemyX = [50]
enemyY = [50]
enemyX_change = []
enemyY_change = []
num_of_enemies = 44

for i in range(num_of_enemies):
    n = i + 1
    enemyImg.append(pygame.image.load('enemy.png'))
    if n % 11 == 0:
        enemyX.append(50)
        enemyY.append(enemyY[i - 1] + 50)
    else:
        enemyX.append(enemyX[i] + 40)
        enemyY.append(enemyY[i])
    enemyX_change.append(0.5)
    enemyY_change.append(20)

# player bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

#player1 bullet
player_bulletImg = pygame.image.load('player_bullet.png')
player1_bulletX = 0
player1_bulletY = 480
player1_bulletX_change = 0
player1_bulletY_change = 2
player1_bullet_state = "ready"

#player2 bullet
player2_bulletX = 0
player2_bulletY = 480
player2_bulletX_change = 0
player2_bulletY_change = 2
player2_bullet_state = "ready"

#enemy bullet
enemy_bulletImg = pygame.image.load('enemy_bullet.png')
enemy_bulletX = 0
enemy_bulletY = 480
enemy_bulletX_change = 0
enemy_bulletY_change = 0.5
enemy_bullet_state = "ready"

#server should decide the first one log in would be player1
#in this script should have bool FirstLogIn, if true player1, else player2
# Player1
player1Img = pygame.image.load('player.png')
player1X = 300
player1Y = 480
player1X_change = 0
# Player2
player2Img = pygame.image.load('player2.png')
player2X = 500
player2Y = 480
player2X_change = 0

player_vel = 0.5

# score
score_value = 0
fonts = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

# lives
live_value = 5
fontl = pygame.font.Font('freesansbold.ttf', 32)
liveX = 650
liveY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = fonts.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_live(x,y):
    life = fontl.render("Lives :" + str(live_value), True, (255, 255, 255))
    screen.blit(life, (x, y))

def game_over_text():
    over_text = fonts.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(player, x, y):
    screen.blit(player, (x, y))  # blit means to draw

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit means to draw

def bunker(x, y, i):
    screen.blit(bunkerImg[i], (x, y))

def fire_player1_bullet(x, y):
    global player1_bullet_state
    player1_bullet_state = "fire"
    screen.blit(player_bulletImg, (x + 17, y + 10))
def fire_player2_bullet(x, y):
    global player2_bullet_state
    player2_bullet_state = "fire"
    screen.blit(player_bulletImg, (x + 17, y + 10))


def isCollision(X1, Y1, X2, Y2):
    distance = math.sqrt(math.pow(X1 - X2, 2) + math.pow(Y1 - Y2, 2))
    if distance < 27:
        return True
    else:
        return False

FirstLogIn = True #get data from server
# Game Loop
running = True
while running:

    # RGB Red, Green, Blue color
    screen.fill((0, 0, 0))

    for event in pygame.event.get():  # check all the events in the window
        if event.type == pygame.QUIT:
            running = False
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT] and player1X - player_vel > 0: # left
        #     player1X -= player_vel
        # if keys[pygame.K_RIGHT] and player1X + player_vel + player1Img.get_width() < width: # right
        #     player1X += player_vel
        # if keys[pygame.K_a] and player2X - player_vel > 0: # left
        #     player2X -= player_vel
        # if keys[pygame.K_d] and player2X + player_vel + player2Img.get_width() < width: # right
        #     player2X += player_vel
        # if keys[pygame.K_SPACE]:
        #     if player1_bullet_state == "ready":
        #         # get the current x coordinate of the spaceship
        #         player1_bulletX = player1X
        #         fire_player1_bullet(player1_bulletX, player1_bulletY)
        # if keys[pygame.K_TAB]:
        #     if player2_bullet_state == "ready":
        #         # get the current x coordinate of the spaceship
        #         player2_bulletX = player2X
        #         fire_player2_bullet(player2_bulletX, player2_bulletY)

        # # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1X_change = -0.5
            if event.key == pygame.K_RIGHT:
                player1X_change = 0.5
            if event.key == pygame.K_a:
                player2X_change = -0.5
            if event.key == pygame.K_d:
                player2X_change = 0.5
            if event.key == pygame.K_SPACE:
                if player1_bullet_state == "ready":
                    # get the current x coordinate of the spaceship
                    player1_bulletX = player1X
                    fire_player1_bullet(player1_bulletX, player1_bulletY)
            if event.key == pygame.K_TAB:
                if player2_bullet_state == "ready":
                    # get the current x coordinate of the spaceship
                    player2_bulletX = player2X
                    fire_player2_bullet(player2_bulletX, player2_bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1X_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2X_change = 0

                

    # checking for boundaries of spaceship sp it doesn't go out of bounds
    player1X += player1X_change
    player2X += player2X_change

    if player1X <= 0:
        player1X = 0
    elif player1X >= 730:
        player1X = 730

    if player2X <= 0:
        player2X = 0
    elif player2X >= 730:
        player2X = 730

    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)
    
    for i in range(num_of_bunker):
        bunker(BunkerX[i], BunkerY[i], i)

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 400:
            live_value = 0

        if live_value == 0:
            for j in range(num_of_enemies):
                enemyY[j] = -2000
            game_over_text()
            break

        if enemyX[i] == 1000:
            enemyX_change[i] = 0
            enemyY_change[i] = 0

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 20:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]


        # collision detection
        KillEnemyCollision1 = isCollision(enemyX[i], enemyY[i], player1_bulletX, player1_bulletY)
            
        KillEnemyCollision2 =  isCollision(enemyX[i], enemyY[i], player2_bulletX, player2_bulletY)
           
        if KillEnemyCollision1:
            player1_bulletY = 480
            player1_bullet_state = "ready"
            score_value += 10
            #print(score_value)
            # removes enemy out of screen
            enemyX[i] = 1000
            enemyY[i] = -1000
        if KillEnemyCollision2:
            player2_bulletY = 480
            player2_bullet_state = "ready"
            enemyX[i] = 1000
            enemyY[i] = -1000
            #enemyImg.pop(i)
            #num_of_enemies -= 1
    # player1_bullet movement
    if player1_bulletY <= -10:
        player1_bulletY = 480
        player1_bullet_state = "ready"

    if player1_bullet_state == "fire":
        fire_player1_bullet(player1_bulletX, player1_bulletY)
        player1_bulletY -= player1_bulletY_change
    if player2_bulletY <= -10:
        player2_bulletY = 480
        player2_bullet_state = "ready"

    if player2_bullet_state == "fire":
        fire_player2_bullet(player2_bulletX, player2_bulletY)
        player2_bulletY -= player2_bulletY_change

    
    player(player1Img, player1X, player1Y)#draw player1
    player(player2Img, player2X, player2Y)#draw player2
    show_score(scoreX, scoreY)
    show_live(liveX, liveY)
    pygame.display.update()
