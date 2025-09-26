# Добавление данных в файл
with open('data.txt', 'a') as file:
    file.write('\nAppending new line.')

# Чтение данных из файла
with open('data.txt', 'r') as file:
    content = file.read()
    print(content)