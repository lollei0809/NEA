import pygame
from pygame.rect import *
import time

pygame.init()
screen = pygame.display.set_mode([750, 750])
rect = Rect(100,10,500,50)
rect1=Rect(100,10,500,50)
run = True
a=[0,1]
moving_rect = rect
color=(0,0,0)
bottom_lim=700

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                print("clicked")
                color=(255,255,255)
                bottom_lim +=50

    moving_rect.move_ip(a)
    while moving_rect.bottom > bottom_lim:
        moving_rect = rect1
        bottom_lim -= 50


    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255,0,0), rect1)
    pygame.display.flip()

pygame.quit()
