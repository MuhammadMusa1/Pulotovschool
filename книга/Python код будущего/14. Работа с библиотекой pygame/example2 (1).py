import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Рисование фигур")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Заполнение экрана белым цветом

    pygame.draw.rect(screen, (0, 128, 255), (30, 30, 60, 60))
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 50)

    pygame.display.flip()

pygame.quit()