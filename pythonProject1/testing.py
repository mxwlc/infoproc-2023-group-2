import pygame
import random
import math
import sys
from button import Button


pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
menu_bg = pygame.image.load('menu_bg.png')# images
pygame.display.set_caption("Menu")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
font = pygame.font.SysFont('arialblack', 35)# fonts
fontl = pygame.font.SysFont('cambria', 64)
fonts = pygame.font.SysFont('arialblack', 20)
over_font = pygame.font.SysFont('arialblack', 72)
text_colour = (255, 255, 255)# colours


class Bunker:
    def __init__(self, X, Y, Health):
        self.X = X
        self.Y = Y
        self.Health = Health

    def draw(self):
        image = pygame.image.load('bunker.png')
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

#enemy grid 
enemyImg = []
enemyX_change = []
enemyY_change = [] 
enemyX = [50]
enemyY = [50]
num_of_enemies = 44

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))


# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('player_bullet.png')
bulletY_change = 5
player1_bulletX = 0 # player1 bullet
player1_bulletY = 500
player2_bulletX = 0 # player2 bullet
player2_bulletY = 500
enemy_bulletImg = pygame.image.load('enemy_bullet.png') # enemy bullet
enemy_bulletX = 0
enemy_bulletY = 500
enemy_bulletY_change = 5
enemy_bullet_state = "ready"

# Player1
player1Img = pygame.image.load('player.png') 
player1X_change = 0
Player1 = Player(300, 500, 5, 0, "ready", bulletImg)
score_value1 = Player1.Score # player 1 score
live_value1 = Player1.Lives

# Player2/remote player
player2Img = pygame.image.load('player2.png')
player2X_change = 0
Player2 = Player(500, 500, 5, 0, "ready", bulletImg)
score_value2 = Player2.Score 
live_value2 = Player2.Lives

# velocity
player_vel = 2
enemy_vel = 1

# bunker 
bunker_health = 4
bunker_width = pygame.image.load('bunker.png').get_width()
space = (width -80 - bunker_width*4)/3 + bunker_width
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


def enemy_attack(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletImg, (x + 16, y + 10))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def show_my_score(score_value1):
    score = fonts.render("Score :" + str(score_value1), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def show_other_score(score_value2):
    score = fonts.render("Other Player Score :" + str(score_value2), True, (255, 255, 255))
    screen.blit(score, (10, 30))


def show_live(live_value1):
    life = fonts.render("Lives :" + str(live_value1), True, (255, 255, 255))
    screen.blit(life, (550, 10))


def show_other_live(live_value2):
    life = fonts.render("Other Player Lives :" + str(live_value2), True, (255, 255, 255))
    screen.blit(life, (550, 30))

def game_over_screen(I_Won):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (width/2 - over_text.get_width()/2, 150))
    win = fonts.render("You Win!", True, (255, 255, 255))
    lose = fonts.render("You Lose", True, (255, 255, 255))
    if I_Won:
        screen.blit(win, (width/2-win.get_width()/2, 300))
    else:
        screen.blit(lose, (width/2-win.get_width()/2, 300))


def boundary(X1):
    if X1 <= 0:
        X1 = 0
    elif X1 >= 730:
        X1 = 730
    return X1


unavailable = []
killed = 0
def LevelUpReset():
    global unavailable, killed 
    unavailable.clear()
    killed = 0

def NewGameReset():
    global Player1, Player2, bunkers, player1X_change, player2X_change, score_value1, live_value1, score_value2, live_value2, enemy_vel
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
        bunkers[i].X = 40 + space*i 
        bunkers[i].Health = bunker_health


def EnemyLevelUp(): #reset positions and bodycount
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

def play():
    # add fps to synchronise the game on different devices
    clock = pygame.time.Clock()
    fps = 60
    NewGameReset()
    EnemyLevelUp()
    # Game Loop
    global player1X_change, player2X_change, enemy_bullet_state, player1_bulletX, player2_bulletX, enemy_bulletX, enemy_bulletY, player1_bulletY, player2_bulletY, killed, unavailable, enemy_vel
    running = True
    over = False
    I_Won = False

    while running:
        # RGB Red, Green, Blue color
        screen.fill((0, 0, 0))

        for event in pygame.event.get():  # check all the events in the window
            if event.type == pygame.QUIT:
                running = False
            # # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1X_change = -player_vel
                if event.key == pygame.K_RIGHT:
                    player1X_change = player_vel
                if event.key == pygame.K_a:
                    player2X_change = -player_vel
                if event.key == pygame.K_d:
                    player2X_change = player_vel
                if event.key == pygame.K_SPACE:
                    if Player1.Bullet_State == "ready":
                        player1_bulletX = Player1.X
                        Player1.shoot(player1_bulletX, player1_bulletY)
                if event.key == pygame.K_TAB:
                    if Player2.Bullet_State == "ready":
                        player2_bulletX = Player2.X
                        Player2.shoot(player2_bulletX, player2_bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1X_change = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player2X_change = 0

        # checking for boundaries of spaceship sp it doesn't go out of bounds
        Player1.X += player1X_change
        Player2.X += player2X_change
        Player1.X = boundary(Player1.X)
        Player2.X = boundary(Player2.X)

        #random shooting from enemy
        if random.randint(0, 100) < 10:
            if enemy_bullet_state == "ready":
                rand_num = random.randint(0, 43)
                while rand_num in unavailable:
                    rand_num = random.randint(0, 43) #the enemy corresponfing to that number will shoot
                enemy_bulletX = enemyX[rand_num]
                enemy_bulletY = enemyY[rand_num]
                enemy_attack(enemy_bulletX, enemy_bulletY)
        # enemy movement
        for i in range(num_of_enemies):
            # game over
            if enemyY[i] > 400:
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
                for j in range(num_of_enemies):
                    enemyY[j] = -2000
                game_over_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - game_over_time < 3000:
                    # Render the game over text
                    game_over_screen(I_Won)
                    pygame.display.update()
                running = False
                start_menu()

            if enemyX[i] == 1000:
                enemyX_change[i] = 0
                enemyY_change[i] = 0

            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 20:
                enemyX_change[i] = enemy_vel
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 730:
                enemyX_change[i] = -enemy_vel
                enemyY[i] += enemyY_change[i]

            # collision detection
            if isCollision(enemyX[i], enemyY[i], player1_bulletX, player1_bulletY):
                player1_bulletY = 500
                Player1.Bullet_State = "ready"
                Player1.add_score(10)
                enemyX[i] = 1000
                enemyY[i] = -1000
                unavailable.append(i)
                killed += 1
            if isCollision(enemyX[i], enemyY[i], player2_bulletX, player2_bulletY):
                player2_bulletY = 500
                Player2.Bullet_State = "ready"
                Player2.add_score(10)
                enemyX[i] = 1000
                enemyY[i] = -1000
                unavailable.append(i)
                killed += 1

            if killed == num_of_enemies:
                EnemyLevelUp()
                enemy_vel += 1

        for i in range(4):
            if isCollision(bunkers[i].X, bunkers[i].Y, enemy_bulletX, enemy_bulletY):
                bunkers[i].lose_health()
                enemy_bulletY = 1000
                # remove bunker from screen

        # player1_bullet movement

        if player1_bulletY <= -5:
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
        if enemy_bulletY >= 610:
            enemy_bulletY = 1000
            enemy_bullet_state = "ready"

        if enemy_bullet_state == "fire":
            enemy_attack(enemy_bulletX, enemy_bulletY)
            enemy_bulletY += enemy_bulletY_change

        # Player1Shot = isCollision(Player1.X, Player1.Y, enemy_bulletX, enemy_bulletY)
        # Player2Shot = isCollision(Player2.X, Player2.Y, enemy_bulletX, enemy_bulletY)
        if isCollision(Player1.X, Player1.Y, enemy_bulletX, enemy_bulletY):
            enemy_bulletY = 1000
            Player1.lose_lives()
        if isCollision(Player2.X, Player2.Y, enemy_bulletX, enemy_bulletY):
            enemy_bulletY = 1000
            Player2.lose_lives()

        Player1.draw(player1Img)  # draw player1
        Player2.draw(player2Img)  # draw player2
        for i in range(num_of_enemies):
            enemy(enemyX[i], enemyY[i], i)
        for bunker in bunkers:
            bunker.draw()

        show_my_score(Player1.Score)
        show_other_score(Player2.Score)
        show_live(Player1.Lives)
        show_other_live(Player2.Lives)
        pygame.display.update()
        clock.tick(fps)


# to be modified
def leaderboard():
    while True:
        lb_text = fonts.render("LEADERBOARD", True, (255, 255, 255))
        screen.blit(lb_text, (200, 250))


def start_menu():
    pygame.display.set_caption('Menu')

    position = [400, 225]  # set initial position

    while True:
        screen.blit(menu_bg, (0, 0))

        menu_text = fontl.render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(400, 100))

        play_button = Button(image=pygame.image.load("Play Rect.png"), pos=(400, 225),
                             text_input="PLAY", font=font, base_color="#b68f40", hovering_color="white")
        leaderboard_button = Button(image=pygame.image.load("Leaderboard Rect.png"), pos=(400, 350),
                                    text_input="LEADERBOARD", font=font, base_color="#b68f40", hovering_color="White")
        quit_button = Button(image=pygame.image.load("Quit Rect.png"), pos=(400, 475),
                             text_input="QUIT", font=font, base_color="#b68f40", hovering_color="#ffffff")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, leaderboard_button, quit_button]:
            button.changeColor(position)
            button.update(screen)

        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_event.type == pygame.KEYUP:
                if menu_event.key == pygame.K_RETURN:
                    if position[1] == 225:  # select play
                        play()
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
    over_text = fonts.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


start_menu()

