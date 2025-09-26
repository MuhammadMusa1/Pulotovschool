# Запись данных в файл
with open('data.txt', 'w') as file:
    file.write('Python is awesome!\n')
    file.write('Files are very useful.')

# Чтение данных из файла
with open('data.txt', 'r') as file:
    content = file.read()
    print(content)