n = int(input())
DB = []
Str = []
for i in range(n):
    name = input('Введите название планеты: ')
    Str.append(name)
    print('Введите информацию о планете', name)
    s = input('Введите массу планеты (тысяч тонн): ')
    Str.append(s)
    s = input('Введите количество спутников у планеты: ')
    Str.append(s)
    s = input('Введите название звезды, вокруг которой обращается планета: ')
    Str.append(s)
    DB.append(Str)
    Str = []

for Str in DB:
    print(Str[0].ljust(10,' '), Str[1].ljust(10,' '),
          Str[2].ljust(5,' '), Str[3].ljust(5,' '))
    
