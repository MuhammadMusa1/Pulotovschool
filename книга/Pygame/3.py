import pygame
class Sprite():
    image = pygame.image.load('Images\Player.png')
    speed = 1
    x = 100
    y = 100
        

w = pygame.display.set_mode ((1279, 700))
Player = Sprite()


game = True                                  
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Player.x += Player.speed
    elif keys[pygame.K_LEFT]:
        Player.x -= Player.speed

    w.fill((0, 0, 0))
    w.blit(Player.image, (Player.x, Player.y))
    pygame.display.update()

pygame.quit ()
