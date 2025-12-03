# Example file showing a basic pygame "game loop"
import pygame

# Load Button Images
def load_images():
    start_img = pygame.image.load("assets/images/Sandy_Start_Button.png").convert_alpha()
    return start_img
    # exit_img = pygame.image.load("Assets/Sandy_Start_Button.png").convert_alpha()

# Class
class button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale)))) # Scale just shrinks the size of the image by the percent you want
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos() # Get mouse position

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False: #0 - left button 1 - middle, 2 - right
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        # Draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
def Menu(screen, color, mouse_rect):
    running = True

    while running:
        screen.fill(color)

        for event in pygame.get_events():
            if event.type == pygame.QUIT:
                running = False
            
        button()

def create_text(screen, text, x, y, font_size, color):
    text = font_size.render(text, True, color)
    text_frame = text.get_rect()
    text_frame.center = (x, y)
    screen.blit(text, text_frame)




# exit_button = Button(450, 200, exit_img, 0.8)

def run(screen, clock, WIDTH, HEIGHT, font_small, SEA_BLUE, WHITE):
    start_img = load_images()
    start_button = button(WIDTH//2, HEIGHT//2, start_img, 5)
    Start = False
    while Start == False:

        screen.fill(SEA_BLUE)
        create_text(screen, f"Kill Zombies to gain points.", WIDTH//2, 100, font_small, WHITE)
        create_text(screen, f"Click on anywhere in the water to create a new island!", WIDTH//2 + 30, 150, font_small, WHITE)
        create_text(screen, f"(For a fee of 10 points, of course...)", WIDTH//2 + 30, 200, font_small, WHITE)
        create_text(screen, f"Use WASD keys to move", WIDTH//2, HEIGHT - 150, font_small, WHITE)
        create_text(screen, f"UP/DOWN/LEFT/RIGHT to shoot, and SPACE to reload.", WIDTH//2, HEIGHT - 100, font_small, WHITE)
        
        if start_button.draw(screen):
            Start = True
        # if exit_button.draw():
        #     running = False
        

        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Start = True

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.update()

        clock.tick(60)  # limits FPS to 60
