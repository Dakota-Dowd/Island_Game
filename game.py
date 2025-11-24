"""
Island Game!
"""

import pygame
import random
import scripts.button_function as button_function
from scripts.button_function import button
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 1000, 900
WHITE = (255,255,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player in the Sea")
clock = pygame.time.Clock()

# Constants
BLACK = (0,0,0)
SEA_BLUE = (0, 105, 148)
GREEN = (0,255,0)
SAND_COLOR = (194, 178, 128)
FPS = 60
font_small = pygame.font.Font("assets/fonts/Kenney Pixel.ttf", 50)
font_large = pygame.font.Font("assets/fonts/Kenney Pixel.ttf", 150)
MAX_BULLETS = 6

"""CLASSES"""


class Player():
    def __init__(self, x, y, width, height, speed, color, lives):
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.lives = lives
        self.player = pygame.image.load("assets/images/Survivor_Image.png")
        self.player = pygame.transform.scale(self.player, (width, height))

        self.hit_counted = False
        self.last_hit_time = pygame.time.get_ticks()

        self.rect = pygame.Rect(x, y, width, height)

    def display(self):
        screen.blit(self.player, self.rect.topleft)

    def update(self, dy, dx):
        # Movement
        self.posx += self.speed * dx
        self.posy += self.speed * dy

        # boundaries
        if self.posx <= 0:
            self.posx = 0
        if self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width
        if self.posy <= 0:
            self.posy = 0
        if self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        # update rect
        self.rect.topleft = (self.posx, self.posy)

    def display_lives(self, text, x, y, lives, color):
        if lives >= 0:
            lives = lives
        else:
            lives = 0

        text = font_small.render(f"{text} {lives}", True, color)
        text_frame = text.get_rect()
        text_frame.topleft = (x, y)
        screen.blit(text, text_frame)

    def hit(self):
        current_time = pygame.time.get_ticks()
        if self.hit_counted == False and current_time - self.last_hit_time > 1000:
            self.lives -= 1
            self.hit_counted = True
            self.last_hit_time = current_time
            
    def get_rect(self):
        return self.rect
    
class Bullet():
    def __init__(self, x, y, width, height, speed, color, dx, dy):
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(x, y, width, height)

    def display(self):
        pygame.draw.rect(screen, BLACK, self.rect)

    def update(self):
        self.posx += self.speed * self.dx
        self.posy += self.speed * self.dy

        self.rect.topleft = (self.posx, self.posy)

    def get_rect(self):
        return self.rect

class Island():
    def __init__(self, x, y):
        self.posx, self.posy = x, y
        self.size = 100
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.sand = pygame.image.load("assets/images/Simple_Sand.png")
        self.sand = pygame.transform.scale(self.sand, (self.size, self.size))
        self.water = pygame.image.load("assets/images/Water_7.png")
        self.water = pygame.transform.scale(self.water, (self.size, self.size))
        self.is_island = False

        # Tree Stuff
        self.tree_size = 40
        random_tree_x = random.randint(1,self.size - self.tree_size)
        random_tree_y = random.randint(1,self.size - self.tree_size)
        self.tree_posx, self.tree_posy = (self.posx + random_tree_x), (self.posy + random_tree_y)
        self.tree_rect = pygame.Rect(self.tree_posx, self.tree_posy, self.tree_size, self.tree_size)
        self.tree = pygame.image.load("assets/images/Tree_Image.png")
        self.tree = pygame.transform.scale(self.tree, (self.tree_size, self.tree_size))

    def display(self):
        if self.is_island == False:
            screen.blit(self.water, self.rect.topleft)
        else:
            screen.blit(self.sand, self.rect.topleft)
            screen.blit(self.tree, self.tree_rect.topleft)


class Zombie():
    def __init__(self, x, y, width, height, speed, color):
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.zombie = pygame.image.load("assets/images/Pirate_Image.png")
        self.zombie = pygame.transform.scale(self.zombie, (width,height))
        self.dy = 0
        self.dx = 0

        self.rect = pygame.Rect(x, y, width, height)

    # def display(self):
    #     pygame.draw.rect(screen, self.color, self.rect)
    def display(self):
        screen.blit(self.zombie, self.rect.topleft)

    def update(self, x_player, y_player):
        # Follow the player
        if x_player <= self.posx: 
            self.dx = -1
        elif x_player >= self.posx:
            self.dx = 1
        if y_player <= self.posy:
            self.dy = -1
        elif y_player >= self.posy:
            self.dy = 1

        # update movement
        self.posx += self.speed * self.dx
        self.posy += self.speed * self.dy

        # update the rect
        self.rect.topleft = (self.posx, self.posy)


    def get_rect(self):
        return self.rect


def create_text(text, x, y, font_size, color):
    text = font_size.render(text, True, color)
    text_frame = text.get_rect()
    text_frame.center = (x, y)
    screen.blit(text, text_frame)

def start_menu(current_time, start_time):
    if current_time - start_time <= 5000:

        # menu = pygame.Rect(WIDTH*.33, HEIGHT*.33, 500, 500)
        # menu.center = (WIDTH//2, HEIGHT//2)
        # pygame.draw.rect(screen, SAND_COLOR, menu)

        create_text(f"Kill Zombies to gain points.", WIDTH//2, 200, font_small, WHITE)
        create_text(f"Click on anywhere in the water to create a new island!", WIDTH//2 + 30, 250, font_small, WHITE)
        create_text(f"(For a fee of 10 points, of course...)", WIDTH//2 + 30, 300, font_small, WHITE)
        create_text(f"Use WASD keys to move", WIDTH//2, 600, font_small, WHITE)
        create_text(f"UP/DOWN/LEFT/RIGHT to shoot, and SPACE to reload.", WIDTH//2, 650, font_small, WHITE)


"""THE GAME"""
def main():
    start_time = pygame.time.get_ticks()
    hit_refesh_time = pygame.time.get_ticks()
    bullet_reload_time = pygame.time.get_ticks() 


    # create Objects
    player = Player(WIDTH//2, HEIGHT//2, 40, 40, 10, WHITE, 3)
    # Initialize variables
    list_islands = []
    list_bullets = []
    list_zombies = []
    dy, dx = 0, 0
    spawn_interval = random.randint(500, 5000)
    ammo_count = 6
    kill_count = 0
    island_size = 100
    points = 0

    # Create squares across the screen
    for x in range(0, WIDTH, island_size):
        for y in range(0, HEIGHT, island_size):
            island = Island(x,y)
            list_islands.append(island)

    # center island
    list_islands[40].is_island = True
    list_islands[49].is_island = True

    running = True
    while running:
        button_function.run
        screen.fill(SEA_BLUE)
        current_time = pygame.time.get_ticks()
   

        for event in pygame.event.get(): # Button Handling
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            # Key Events
            if event.type == pygame.KEYDOWN:
                # Player movement
                if event.key == pygame.K_w:
                    dy = -1
                if event.key == pygame.K_s:
                    dy = 1
                if event.key == pygame.K_a:
                    dx = -1
                if event.key == pygame.K_d:
                    dx = 1

                # Bullet Keys
                if event.key == pygame.K_UP and ammo_count > 0:
                    bullet_dx = 0
                    bullet_dy = -1
                    bullet = Bullet(player.posx, player.posy, 20,20,5, BLACK, bullet_dx, bullet_dy)
                    list_bullets.append(bullet)
                    ammo_count -= 1

                if event.key == pygame.K_DOWN and ammo_count > 0:
                    bullet_dx = 0
                    bullet_dy = 1
                    bullet = Bullet(player.posx, player.posy, 20,20,5, BLACK, bullet_dx, bullet_dy)
                    list_bullets.append(bullet)
                    ammo_count -= 1

                if event.key == pygame.K_LEFT and ammo_count > 0:
                    bullet_dx = -1
                    bullet_dy = 0
                    bullet = Bullet(player.posx, player.posy, 20,20,5, BLACK, bullet_dx, bullet_dy)
                    list_bullets.append(bullet)
                    ammo_count -= 1

                if event.key == pygame.K_RIGHT and ammo_count > 0:
                    bullet_dx = 1
                    bullet_dy = 0
                    bullet = Bullet(player.posx, player.posy, 20,20,5, BLACK, bullet_dx, bullet_dy)
                    list_bullets.append(bullet)
                    ammo_count -= 1

                # Reload with the space button
                if event.key == pygame.K_SPACE and ammo_count <= 0 and current_time - bullet_reload_time >= 1000:
                        ammo_count = 6
                        bullet_reload_time = current_time

            # Stop the player when the keys are lifted
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    dy = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    dx = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 2, 2)
                for island in list_islands:
                    if island.is_island == False and points >= 10:
                        if pygame.Rect.colliderect(mouse_rect, island.rect):
                            island.is_island = True
                            points -= 10


        """DISPLAY"""

        def display_all():
            # display objects
            for island in list_islands:
                island.display()

            player.display()

            # Display Screen Text
            create_text(f"AMMO - {ammo_count}", 100, 50, font_small, WHITE)
            create_text(f"ZOMBIES KILLED: {kill_count}", 165, 100, font_small, WHITE)
            create_text(f"LIVES - {player.lives}", WIDTH - 200, 50, font_small, WHITE)
            create_text(f"POINTS - {points}", 110, 150, font_small, WHITE)

        display_all() # call the function

        """UPDATE"""

        # Display/Update bullets
        for bullet in list_bullets:
                if bullet.posx <= 0 or bullet.posx >= WIDTH or bullet.posy <= 0 or bullet.posy >= HEIGHT:
                    list_bullets.remove(bullet)
                else:
                    bullet.display()
                    bullet.update()

        # update objects
        prev_x = player.posx
        prev_y = player.posy
        player.update(dy, dx)

        # Island collision
        for island in list_islands:
            if island.is_island == False:
                if pygame.Rect.colliderect(island.rect, player.rect):
                    player.posx = prev_x
                    player.posy = prev_y
        
        """Loop through each zombie, then loop through each island that are sand. If is_island = True, then slow down the zombie. Set their speed to something slower"""
        # for zombie in list_zombies:
        #     if pygame.Rect.colliderect(zombie, ):


        # Make a new zombie periodically
        x_zombie = random.randint(0, WIDTH)
        y_zombie = random.randint(0, HEIGHT)
        if current_time - hit_refesh_time >= spawn_interval:
            # Pick a random location for the zombie to spawn
            rand_side = random.randint(1, 4)
            if rand_side == 1:
                zombie = Zombie(0,y_zombie,40, 40, 1, GREEN) # left side
            elif rand_side == 2:
                zombie = Zombie(WIDTH,y_zombie,40, 40, 1, GREEN) # right side
            elif rand_side == 3:
                zombie = Zombie(x_zombie,0,40, 40, 1, GREEN) # top
            else:
                zombie = Zombie(x_zombie, HEIGHT, 40, 40, 1, GREEN) # bottom
            list_zombies.append(zombie)
            hit_refesh_time = current_time
            spawn_interval = random.randint(200, 2000)

        # UPDATE ZOMBIES
        for zombie in list_zombies:
            zombie.display()
            zombie.update(player.posx, player.posy)

            # bullet collision
            for bullet in list_bullets:
                if zombie.rect.colliderect(bullet.get_rect()):
                    list_bullets.remove(bullet)
                    list_zombies.remove(zombie)
                    kill_count += 1
                    points += 1

            # Lose lives when the zombie hits you
            if pygame.Rect.colliderect(player.get_rect(), zombie.get_rect()):

                if player.hit_counted == False:
                    player.hit()
            else:
                player.hit_counted = False #if they aren't touching reset hit_counted to false

        # update screen
        pygame.display.update()
        clock.tick(FPS)
    
        """___END_GAME___"""
        if player.lives == 0:
            display_all()
            create_text("GAME OVER", WIDTH // 2, HEIGHT //2, font_large, WHITE)
            pygame.display.update()
            end_credits = True
            while end_credits:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end_credits = False
            running = False

main()
pygame.quit()
