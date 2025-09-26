#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Asus
#
# Created:     13.04.2020
# Copyright:   (c) Asus 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
def collide(Sprite1, Sprite2):
    if ((     Sprite1.x <=  Sprite2.x  <= Sprite1.x + Sprite1.width
        and   Sprite1.y <= Sprite2.y <= Sprite1.y + Sprite1.height)
        or   (Sprite1.x <= Sprite2.x + Sprite2.width  <= Sprite1.x + Sprite1.width
        and   Sprite1.y <= Sprite2.y + Sprite2.Height <= Sprite1.y + Sprite1.height)
        or   (Sprite2.x <= Sprite1.x + Sprite1.width  <= Sprite2.x + Sprite2.width
        and   Sprite2.y <= Sprite1.y <= Sprite2.y + Sprite2.height)
        or   (Sprite2.x <= Sprite1.x <= Sprite2.x + Sprite2.width
        and   Sprite2.y <= Sprite1.y + Sprite1.height <= Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False
class Const():
    def __init__(self, value):
        self.value = value

class Sprite():
    def __init__(self, x, y, speed, img):

        self.image = pygame.image.load(img)
        self.speed = speed
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speedx = 0
        self.speedy = 0
        self.jumppower = -10
    def setimage(self, img):
        self.image = pygame.image.load(img)


Ncadr = 0
clock = pygame.time.Clock()
g = Const(1)
w = pygame.display.set_mode ((1279, 700))
Player = Sprite(100, 100, 5, 'Images/Player.png')

# animation for go to right
ImgPlayerGoR = [pygame.image.load('Images/GoAnim/b1.png'),
               pygame.image.load('Images/GoAnim/b2.png'),
               pygame.image.load('Images/GoAnim/b3.png'),
               pygame.image.load('Images/GoAnim/b4.png'),
               pygame.image.load('Images/GoAnim/b5.png')]

# animation for go to left
ImgPlayerGoL = []
for img in ImgPlayerGoR:
    ImgPlayerGoL.append(pygame.transform.flip(img, True, False))


Ground = Sprite(80, 400, 0, 'Images/ground.png')


game = True
while game:
    clock.tick(24)
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
            Player.rect.x += Player.speed
            Player.image = ImgPlayerGoR[Ncadr % 5]
    elif keys[pygame.K_LEFT]:
            Player.rect.x -= Player.speed
            Player.image = ImgPlayerGoL[Ncadr % 5]
    if keys[pygame.K_SPACE]:
        if Player.speedy == 0:
            Player.speedy = Player.jumppower


    # gravitation
    if not collide(Player.rect, Ground.rect):
        Player.speedy += g.value

    elif Player.speedy > 0:
        Player.speedy = 0


    Player.rect.y += Player.speedy


    w.fill((0, 0, 0))
    w.blit(Player.image, Player.rect)
    w.blit(Ground.image, Ground.rect)
    pygame.display.update()
    Ncadr += 1

pygame.quit ()

