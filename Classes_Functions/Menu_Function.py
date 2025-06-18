# Menu Function
import pygame
pygame.init()
from Classes_Functions.Button_Function import Button

def Menu(screen, color, mouse_rect):
    running = True

    while running:
        screen.fill(color)

        for event in pygame.get_events():
            if event.type == pygame.QUIT:
                running = False
            
        Button()


