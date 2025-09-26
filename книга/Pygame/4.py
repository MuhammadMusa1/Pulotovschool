import pygame
class Sprite():
    def __init__(self, x, y, speed, img):

        self.image = pygame.image.load(img)
        self.speed = speed
        self.x = x
        self.y = y
        self.imgR  = pygame.image.load(img)
        self.imgL = pygame.transform.flip(self.image, True, False)



##Ncadr = 0
w = pygame.display.set_mode ((1279, 700))
Player = Sprite(100, 100, 1, 'Images/Player.png')
##ImgPlayerGo = [pygame.image.load('Images/GoAnim/b1.png'),
##               pygame.image.load('Images/GoAnim/b2.png'),
##               pygame.image.load('Images/GoAnim/b3.png'),
##               pygame.image.load('Images/GoAnim/b4.png'),
##               pygame.image.load('Images/GoAnim/b5.png')]


game = True
while game:
    for ev in pygame.event.get ():
        if ev.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Player.x += Player.speed
        Player.image = Player.imgR
    elif keys[pygame.K_LEFT]:
        Player.x -= Player.speed
        Player.image = Player.imgL


    w.fill((0, 0, 0))
    #w.blit(ImgPlayerGo[Ncadr % 5], (Player.x, Player.y))
    w.blit(Player.image, (Player.x, Player.y))
    pygame.display.update()
##    Ncadr += 1

pygame.quit ()
