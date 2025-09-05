import os
import time
import random

# Размеры экрана
WIDTH = 60
HEIGHT = 20

# Инициализация звездного поля
stars = []

# Создаем начальные звезды
def init_stars():
    for _ in range(20):  # Количество звезд
        star = {
            'x': random.randint(0, WIDTH - 1),
            'y': random.randint(0, HEIGHT - 1),
            'speed': random.uniform(0.1, 0.5)
        }
        stars.append(star)

# Отрисовка экрана
def draw_screen():
    screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for star in stars:
        if 0 <= int(star['y']) < HEIGHT and 0 <= int(star['x']) < WIDTH:
            screen[int(star['y'])][int(star['x'])] = '*'
    
    # Вывод экрана
    os.system('cls' if os.name == 'nt' else 'clear')  # Очистка терминала
    for row in screen:
        print(''.join(row))

# Обновление позиций звезд
def update_stars():
    for star in stars:
        star['y'] += star['speed']  # Движение вниз
        if star['y'] >= HEIGHT:  # Если звезда вышла за пределы, перезапускаем
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH - 1)
            star['speed'] = random.uniform(0.1, 0.5)

# Основной цикл
def main():
    init_stars()
    print("Нажмите Ctrl+C для выхода")
    try:
        while True:
            draw_screen()
            update_stars()
            time.sleep(0.1)  # Скорость анимации
    except KeyboardInterrupt:
        print("\nАнимация завершена!")

if __name__ == "__main__":
    main()