print('---Склад магазина---')
print()

result = 0
for i in range(7):
    print('Сколько компьютеров привезли в день', i + 1, ': ')
    nget = int(input())
    print('Сколько компьютеров продали в день ', i + 1, ': ')
    nsale = int(input())
    result = result + nget - nsale

print('На складе осталось', result, 'компьютеров')
