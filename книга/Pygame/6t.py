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
    if ((Sprite1.x <  Sprite2.x  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y < Sprite1.y + Sprite1.height)
        or   (Sprite1.x < Sprite2.x + Sprite2.width  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y + Sprite2.Height < Sprite1.y + Sprite1.height)
        or   (Sprite2.x < Sprite1.x < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y < Sprite2.y + Sprite2.height)
        or   (Sprite2.x < Sprite1.x + Sprite1.width  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y + Sprite1.height < Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False

class Sprite():
    def __init__(self, x, y, speed, img):

        self.image = pygame.image.load(img)
        self.speed = speed
        self.x = x
        self.y = y
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
    def setimage(self, img):
        self.image = pygame.image.load(img)


Ncadr = 0
w = pygame.display.set_mode ((1279, 700))
Player = Sprite(100, 100, 1, 'Images/Player.png')
ImgPlayerGo = [pygame.image.load('Images/GoAnim/b1.png'),
               pygame.image.load('Images/GoAnim/b2.png'),
               pygame.image.load('Images/GoAnim/b3.png'),
               pygame.image.load('Images/GoAnim/b4.png'),
               pygame.image.load('Images/GoAnim/b5.png')]

Tree = Sprite(400, 100, 0, 'Images/Tree.png')


game = True
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    # test for collide
    if collide(Player, Tree):
        Tree.setimage('Images/Player.png')

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Player.x += Player.speed
    elif keys[pygame.K_LEFT]:
        Player.x -= Player.speed

    w.fill((0, 0, 0))
    w.blit(ImgPlayerGo[Ncadr % 5], (Player.x, Player.y))
    w.blit(Tree.image, (Tree.x, Tree.y))
    pygame.display.update()
    Ncadr += 1

pygame.quit ()

