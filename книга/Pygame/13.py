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
import random
pygame.init()
WorldWidth = 1200 # ширина игрового мира
WorldHeight = 1800 # высота игрового мира
ScreenWidth = 900 #ширина окна программы
ScreenHeight = 600 #высота окна программы
Stage = 0 #этап игры, 0 - стартовое меню, 1 - первый уровень и т. д.
Timer = 0


def ShowCollide(Group, w):
    for Spr in Group.sprites():
        pygame.draw.rect(w, (0, 200, 64), Spr.collider, 3)
def collide(Sprite1, Sprite2):
    if      ((Sprite1.x < Sprite2.x                  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y                  < Sprite1.y + Sprite1.height)
        or   (Sprite1.x < Sprite2.x + Sprite2.width  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y + Sprite2.height < Sprite1.y + Sprite1.height)
        or   (Sprite2.x < Sprite1.x + Sprite1.width  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y                  < Sprite2.y + Sprite2.height)
        or   (Sprite2.x < Sprite1.x                  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y + Sprite1.height < Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False

def collideG(Rect, Group):
    Iscollide = False
    for Spr in Group.sprites():
        if collide(Rect, Spr.collider):
            Iscollide = True
            Group.zrect = Spr.collider
    return Iscollide

def collideGFrwd(Rectin, Group, speedx, speedy):
    Rect = pygame.Rect(0, 0, Rectin.width, Rectin.height)
    Rect.x = Rectin.x + speedx + 1
    Rect.y = Rectin.y + speedy + 1
    return collideG(Rect, Group)

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
        self.collider = self.rect.copy()
    def setimage(self, img):
        self.image = pygame.image.load(img)

class Player(Sprite):
    def __init__(self, x, y, img, GoL, GoR):
        Sprite.__init__(self, x, y, img)
        self.image = pygame.image.load(img)
        self.imgR  = pygame.image.load(img)
        self.imgL = pygame.transform.flip(self.image, True, False)
        self.imgshock = pygame.image.load('Images/Playershok.png')
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speedx = 10
        self.speedy = 0
        self.jumppower = -20
        self.cadr = 0
        self.animGoL = GoL
        self.animGoR = GoR
        self.dir = True # True - right, False - left
        self.health = 100
        self.shock = False

    def update(self, keys, g, GrPlatf, GrFireBall):
        global Timer, Stage
        if self.shock:
            self.image = self.imgshock
            Timer += clock.get_time()
            if Timer > 2000:
                self.shock = False
                Timer = 0


        elif keys[pygame.K_RIGHT] and not collideGFrwd(self.rect, GrPlatf, self.speedx, self.speedy):
            self.speedx = 10
            if self.rect.x + self.rect.width + self.speedx < WorldWidth:
                self.rect.x += self.speedx
            self.image = self.animGoR[self.cadr // 2 % 5]
            self.dir = True
        elif keys[pygame.K_LEFT] and not collideGFrwd(self.rect, GrPlatf, self.speedx-1, self.speedy):
            self.speedx = -10
            if self.rect.x + self.speedx > 0:
                self.rect.x += self.speedx
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

        if not collideGFrwd(self.rect, GrPlatf, 0, self.speedy + g.value):
            self.speedy += g.value
        elif self.speedy > 0:
            self.rect.y = GrPlatf.zrect.y - self.rect.height - 1
            self.speedy = 0

        if collideG(self.rect, GrFireBall) and not self.shock:
            self.health -= 10
            if self.health <= 0:
                Stage = 2
            self.shock = True


        # gravitation
        self.rect.y += self.speedy
        self.collider = self.rect
        self.cadr += 1


class Platform(Sprite):
    def __init__(self, x, y, img, time, group):
        Sprite.__init__(self, x, y, img)
        self.time = time
        self.add(group)
        self.collider.y += 20
        self.collider.height = 60


class Fireball(Sprite):
    def __init__(self, img, group):
        Sprite.__init__(self, 0, 0, 'Images/fireball.png')
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (180, 65)), -90)
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.add(group)
        #self.visible = False
        self.speedx = random.randint(-5, 5)
        self.animimg = img
        self.cadr = 0



    def update (self, g):
        if self.rect.y < WorldHeight - self.rect.height:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            self.speedy += g.value
        else:
            self.rect.y = 0
            self.rect.x = random.randint(0, WorldWidth)
            self.speedx = random.randint(-5, 5)
            self.speedy = random.randint(0, 30)
        self.image = self.animimg[self.cadr // 2 % 4]
        self.cadr += 1
        self.collider = self.rect

class Group(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.zrect = 0

class Camera():
    def __init__(self, sprite):
        self.x = 0
        self.y = -800
    def update(self, sprite):
        #if (self.x < 0 and not sprite.dir and sprite.rect.x<750) or (sprite.dir and self.x > -300 and sprite.rect.x>450) :
        if sprite.rect.x < WorldWidth - ScreenWidth/2 and sprite.rect.x > ScreenWidth/2:
            self.x = int(ScreenWidth/2) - sprite.rect.x

        if sprite.rect.y < WorldHeight - ScreenHeight/2 and sprite.rect.y > ScreenHeight/2:
            self.y = ScreenHeight/2 - sprite.rect.y
class Menu(Sprite):
    pass

# Lesson 12
class Button(Sprite):
    def __init__(self, x, y, img, ImgOnHover, ImgOffHover):
        Sprite.__init__(self, x, y, img)
        self.ImgOnHover = ImgOnHover
        self.ImgOffHover = ImgOffHover

    def update(self):
        if (self.rect.x < pygame.mouse.get_pos()[0] < self.rect.x + self.rect.width
        and self.rect.y < pygame.mouse.get_pos()[1] < self.rect.y + self.rect.height):
            if pygame.mouse.get_pressed()[0]:
                self.onclick()
            else:
                self.hover()
        else:
            self.nothover()

    def hover(self):
        self.image = self.ImgOnHover
    def nothover(self):
        self.image = self.ImgOffHover
    def onclick(self):
        global Stage
        Stage = 1



# игровые часы
clock = pygame.time.Clock()

# menu
menu = Menu(0, 0, 'Images/startscreen.jpg')
# button start
buttonstart = Button(300, 300, 'Images/start.png', pygame.image.load('Images/starton.png'), pygame.image.load('Images/start.png'))

# ускорение свободного падения, объект класса констант
g = Const(1)

#создаем окно программы и получаем доступ к главной поверхности окна, ее имя теперь - w
w = pygame.display.set_mode ((ScreenWidth, ScreenHeight))

# создаем поверхность игрвого мира, на которой будем рисовать всех спрайтов
world = pygame.Surface((WorldWidth, WorldHeight))

# создаем объект - шрифт, с помощью которого будем выводить надписи в игре
font = pygame.font.Font(None, 25)
fontLooser = pygame.font.Font(None, 45)


GroupPlatform = Group()
GroupFireBall = Group()


#Platforms
Ground1 = Platform(80,  1200, 'Images/ground.png', 100, GroupPlatform)
Ground2 = Platform(380, 1000, 'Images/ground.png', 100, GroupPlatform)
Ground3 = Platform(780, 800, 'Images/ground.png', 100, GroupPlatform)
Ground4 = Platform(80,  500, 'Images/ground.png', 100, GroupPlatform)

# lava
Lava = Platform(0,  1800 - 110, 'Images/lava.png', 100, GroupPlatform)
pygame.transform.scale(Lava.image, (1200, 110))


ImgPlayerGoR = [pygame.image.load('Images/GoAnim/b1.png'),
               pygame.image.load('Images/GoAnim/b2.png'),
               pygame.image.load('Images/GoAnim/b3.png'),
               pygame.image.load('Images/GoAnim/b4.png'),
               pygame.image.load('Images/GoAnim/b5.png')]

ImgPlayerGoL = []

ImgFireBall = [pygame.image.load('Images/fireball.png'),
                pygame.image.load('Images/fireball1.png'),
                pygame.image.load('Images/fireball2.png'),
                pygame.image.load('Images/fireball3.png'),]
i = 0
for img in ImgFireBall:
    ImgFireBall[i] = pygame.transform.rotate(pygame.transform.scale(img, (180, 65)), -90)
    i += 1


for img in ImgPlayerGoR:
    ImgPlayerGoL.append(pygame.transform.flip(img, True, False))

Player = Player(100, 1100, 'Images/Player.png', ImgPlayerGoL, ImgPlayerGoR)

# создаем камеру
cam = Camera(Player)

Tree = Sprite(400, 100, 'Images/Tree.png')

# создаем огненные шары
Fb1 = Fireball(ImgFireBall, GroupFireBall)
Fb2 = Fireball(ImgFireBall, GroupFireBall)
Fb3 = Fireball(ImgFireBall, GroupFireBall)
Fb4 = Fireball(ImgFireBall, GroupFireBall)



game = True
while game:
    clock.tick(24)
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False


    keys = pygame.key.get_pressed()

    # start menu
    if Stage == 0:
        buttonstart.update()
        w.blit(menu.image, (menu.rect.x, menu.rect.y))
        w.blit(buttonstart.image, (buttonstart.rect.x, buttonstart.rect.y))

    # first stage
    elif Stage == 1:
        Player.update(keys, g, GroupPlatform, GroupFireBall)
        w.fill((0, 0, 0))
        world.fill((0, 0, 0))
        world.blit(Player.image, Player.rect)
        #w.blit(Tree.image, Tree.rect)
        GroupPlatform.draw(world)
        GroupFireBall.update(g)
        ShowCollide(GroupFireBall, world)
        GroupFireBall.draw(world)
        text = font.render(str(Player.health),True,(0, 255, 0))
        world.blit(text, (50-cam.x, 50-cam.y))
        cam.update(Player)

        w.blit(world, (cam.x, cam.y))
    elif Stage == 2:
        text = fontLooser.render('LOOSER',True,(252, 58, 58))
        w.blit(text, (int(ScreenWidth/2), int(ScreenHeight/2)))
        Timer += clock.get_time()
        if Timer > 3000:
            Timer = 0
            Stage = 0

    pygame.display.update()


pygame.quit ()

