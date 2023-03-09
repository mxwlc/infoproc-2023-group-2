import pygame
import os
import time
import random
from player1send import *

pygame.font.init()

WIDTH, HEIGHT = 750, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    player1lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 4
    enemy_vel = 2

    player_vel = 6
    laser_vel = 6

    player = Player(300, 530)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {player1lives}", 1, (255,255,255))
        player2lives_label = main_font.render(f"player2lives: {player2lives}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(player2lives_label, (WIDTH - player2lives_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player1lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
                
            else:
                continue


        if len(enemies) == 0:
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        #if keys[pygame.K_UP] and player.y - player_vel > 0: # up
           # player.y -= player_vel
        #if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
           # player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 4*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy) #if player collide with enemy health -10
            elif enemy.y + enemy.get_height() > HEIGHT:
                player1lives -= 1
                enemies.remove(enemy) #if player misses an enemy lives -1

        player.move_lasers(-laser_vel, enemies)

def homepage():
    title_font = pygame.font.SysFont("comicsans", 50)
    title_label1 = title_font.render("Welcome to Space Invaders", 1, (255,0,0))
    title_label2 = title_font.render("Press Enter to Start", 1, (255,255,255))
    title_label3 = title_font.render("Or press space for tutorial", 1, (255,255,255))
    WIN.blit(title_label1, (WIDTH/2 - title_label1.get_width()/2, 100))
    WIN.blit(title_label2, (WIDTH/2 - title_label2.get_width()/2, 250))
    WIN.blit(title_label3, (WIDTH/2 - title_label3.get_width()/2, 300))
    pygame.display.update()

def tutorial():
    tutorial_font = pygame.font.SysFont("comicsans", 30)
    tutorial1 = tutorial_font.render("Welcome to the tutorial!", 1, (255, 255, 255)) 
    tutorial2 = tutorial_font.render("Use the arrow keys to move", 1, (255, 255, 255))    
    tutorial3 = tutorial_font.render("and the space bar to shoot.", 1, (255, 255, 255))
    tutorial4 = tutorial_font.render("(hit Enter to start the game)", 1, (255, 255, 255))    
    WIN.blit(tutorial1, (WIDTH/2 - tutorial1.get_width()/2, 200)) 
    WIN.blit(tutorial2, (WIDTH/2 - tutorial2.get_width()/2, 250)) 
    WIN.blit(tutorial3, (WIDTH/2 - tutorial3.get_width()/2, 300)) 
    WIN.blit(tutorial4, (WIDTH/2 - tutorial4.get_width()/2, 400))
    pygame.display.update()

def main_menu():
    run = True
    current_screen = 0
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #if quit the screen game stop running
                current_screen = 0
            if event.type == pygame.KEYDOWN:
                K = pygame.key.get_pressed()
                if K[pygame.K_RETURN]:
                    # If Enter is pressed start game
                    current_screen = 0
                    main()
                elif K[pygame.K_SPACE]:
                    if current_screen == 0: # If space is pressed on the start screen, switch to the tutorial screen
                        current_screen = 1

        WIN.blit(BG, (0,0))
        if current_screen == 0:
            homepage()
        elif current_screen == 1:
            tutorial()        
    pygame.quit()
    
main_menu()