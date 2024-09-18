import pygame
from pygame.rect import *
import time

pygame.init()
screen = pygame.display.set_mode([750, 650])
rectangles = []
for i in range(2):
    rectangles.append(Rect(100, 10, 500, 50))
run = True
a = [0, 1]
moving_rect = rectangles[0]
color = (0, 0, 0)
bottom_lim = 600
i = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for item in rectangles:
                if item.collidepoint(event.pos):
                    print("clicked inside")
                    color = (146, 36, 183)
                    bottom_lim += 50
                    a = [1, 0]
                else:
                    print("clicked outside")
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, color, rectangles[0])
    pygame.draw.rect(screen, (255, 0, 0), rectangles[1])

    moving_rect.move_ip(a)
    # time.sleep(0.001)
    i+=1
    if moving_rect.bottom > bottom_lim:
        if i<=len(rectangles):
            print(i)
            moving_rect = rectangles[i]
            bottom_lim -= 50
        else:
            print(i,len(rectangles))
            a=[0,0]

    pygame.display.flip()

pygame.quit()  
