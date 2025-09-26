import pygame
w = pygame.display.set_mode ((1280, 700))
game = True
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
pygame.quit ()
