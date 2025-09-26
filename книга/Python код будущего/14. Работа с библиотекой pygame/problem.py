import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Анимация")

x = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Заполнение экрана белым цветом

    pygame.draw.circle(screen, (255, 0, 0), (x, 240), 50)
    x += 1
    if x > 640:
        x = 0

    pygame.display.flip()

pygame.quit()