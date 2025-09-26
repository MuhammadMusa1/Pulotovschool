import pygame
w = pygame.display.set_mode ((1279, 700))
Player = pygame.image.load('Images/Player.png')

x =100
y = 100

game = True                                  
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += 5

    w.fill((0, 0, 0))
    w.blit(Player, (x, y))
    pygame.display.update()

pygame.quit ()
