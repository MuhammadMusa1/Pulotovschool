import datetime
import os
import random

# Получение текущей даты и времени
now = datetime.datetime.now()
print(f"Текущая дата и время: {now}")

# Получение списка файлов в текущей директории
files = os.listdir('.')
print(f"Файлы в текущей директории: {files}")

# Генерация случайного числа
random_number = random.randint(1, 100)
print(f"Случайное число: {random_number}")