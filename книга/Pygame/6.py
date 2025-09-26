import pygame
# вспомогательная функция, показывает коллайдер спрайто
def ShowCollide(Spr, w):
    pygame.draw.rect(w, (0, 200, 64), Spr, 3)

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

class Sprite():
    def __init__(self, x, y, speed, img):
        self.speed = speed
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft = (x, y))
    def setimage(self, img):
        self.image = pygame.image.load(img)


Ncadr = 0
w = pygame.display.set_mode ((1279, 700))
Player = Sprite(100, 100, 1, 'Images/Player.png')

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

# тестовый спрайт - Дерево
Tree = Sprite(400, 100, 0, 'Images/Tree.png')

# Игрвой цикл
game = True
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    # test for collide
    if collide(Player.rect, Tree.rect):
        Tree.setimage('Images/Player.png')
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            Player.rect.x += Player.speed
            Player.image = ImgPlayerGoR[Ncadr % 5]
        elif keys[pygame.K_LEFT]:
            Player.rect.x -= Player.speed
            Player.image = ImgPlayerGoL[Ncadr % 5]

    w.fill((0, 0, 0))
    w.blit(Player.image, Player.rect)
    w.blit(Tree.image, Tree.rect)
    #ShowCollide(Player.rect, w)
    #ShowCollide(Tree.rect, w)
    pygame.display.update()
    Ncadr += 1

pygame.quit ()
