# Запись имен в файл
with open('names.txt', 'w') as file:
    file.write('Alice\n')
    file.write('Bob\n')
    file.write('Charlie\n')

# Чтение имен из файла и запись в другой файл
with open('names.txt', 'r') as infile, open('names_copy.txt', 'w') as outfile:
    for line in infile:
        outfile.write(line)

# Чтение данных из нового файла
with open('names_copy.txt', 'r') as file:
    content = file.read()
    print(content)