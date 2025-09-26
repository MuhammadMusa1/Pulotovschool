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
        and   Sprite1.y < Sprite2.y + Sprite2.height < Sprite1.y + Sprite1.height)
        or   (Sprite2.x < Sprite1.x < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y < Sprite2.y + Sprite2.height)
        or   (Sprite2.x < Sprite1.x + Sprite1.width  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y + Sprite1.height < Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False

def collideG(Sprite, Group):
    Iscollide = False
    for Spr in Group.sprites():
        if collide(Sprite.rect, Spr.rect):
            Iscollide = True
    return Iscollide

class Const():
    def __init__(self, value):
        self.value = value

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speedx = 0
        self.speedy = 0
    def setimage(self, img):
        self.image = pygame.image.load(img)

class Player(Sprite):
    def __init__(self, x, y, img, GoL, GoR):
        Sprite.__init__(self, x, y, img)
        self.image = pygame.image.load(img)
        self.imgR  = pygame.image.load(img)
        self.imgL = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speedx = 5
        self.speedy = 0
        self.jumppower = -10
        self.cadr = 0
        self.animGoL = GoL
        self.animGoR = GoR
        self.dir = True # True - right, False - left
    def update(self, keys, g, GrPlatf):
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            self.image = self.animGoR[self.cadr // 2 % 5]
            self.dir = True
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            self.image = self.animGoL[self.cadr // 2 % 5]
            self.dir = False
        else:
            if self.dir:
                self.image = self.imgR
            else:
                self.image = self.imgL
        if keys[pygame.K_SPACE]:
            if self.speedy == 0:
                self.speedy = self.jumppower

        if not collideG(self, GrPlatf): # rewrite
            self.speedy += g.value
        elif self.speedy > 0:
            self.speedy = 0

        # gravitation
        self.rect.y += self.speedy
        self.collider = self.rect
        self.cadr += 1


class Platform(Sprite):
    def __init__(self, x, y, img, time, group):
        Sprite.__init__(self, x, y, img)
        self.time = time
        self.add(group)


Ncadr = 0
clock = pygame.time.Clock()
g = Const(1)
w = pygame.display.set_mode ((1279, 700))
GroupPlatform = pygame.sprite.Group()
Ground = Platform(80, 400, 'Images/ground.png', 100, GroupPlatform)
Ground1 = Platform(380, 300, 'Images/ground.png', 100, GroupPlatform)


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


Player = Player(100, 100, 'Images/Player.png', ImgPlayerGoL, ImgPlayerGoR)


game = True
while game:
    clock.tick(24)
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False


    keys = pygame.key.get_pressed()


    Player.update(keys, g, GroupPlatform)
    w.fill((0, 0, 0))
    GroupPlatform.draw(w)
    w.blit(Player.image, Player.rect)
    pygame.display.update()
    Ncadr += 1

pygame.quit ()

