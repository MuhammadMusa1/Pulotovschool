import pygame
f = 0
if (f < 0
    and f==9
    and f==9):
        f += 1
class Sprite():
    def __init__(self, x, y, speed, img):

        self.image = pygame.image.load(img)
        self.speed = speed
        self.x = x
        self.y = y


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


game = True
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Player.x += Player.speed
        Player.image = ImgPlayerGoR[Ncadr % 5]
    elif keys[pygame.K_LEFT]:
        Player.x -= Player.speed
        Player.image = ImgPlayerGoL[Ncadr % 5]

    w.fill((0, 0, 0))
    w.blit(Player.image, (Player.x, Player.y))
    pygame.display.update()
    Ncadr += 1

pygame.quit ()
