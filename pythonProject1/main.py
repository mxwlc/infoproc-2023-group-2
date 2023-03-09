import pygame
import random
import math

# Initialize the pygame
pygame.init()

# create the screen, x-axis:800, y-axis:600
screen = pygame.display.set_mode((800, 600))

# background
# background = pygame.image.load('background.png')

# Caption and Ican
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

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

# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.3
bullet_state = "ready"

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

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit means to draw

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB Red, Green, Blue color
    screen.fill((0, 0, 0))

    for event in pygame.event.get():  # check all the events in the window
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundaries of spaceship sp it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730

    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)

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
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            print(score_value)
            # removes enemy out of screen
            enemyX[i] = 1000
            enemyY[i] = -1000

            #enemyImg.pop(i)
            #num_of_enemies -= 1


    # bullet movement
    if bulletY <= -10:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    show_live(liveX, liveY)
    pygame.display.update()
