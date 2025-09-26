# выводит на экран игрвое поле
def show(GF):
    for Str in GF:
        print(Str[0], Str[1], Str[2])

# проверяет строку, одинаковые ли в ней все символы
def TestStr(Str):
    if Str[0] != '-':
        if Str[0] == Str[1] and Str[0] == Str[2]:
            return True
        else:
            return False
    else:
        return False

# проверяет столбец, одинаковые ли в нем все символы
def TestCol(GF, n):
    if GF[0][n] != '-':
        if GF[0][n] == GF[1][n] and GF[0][n] == GF[2][n]:
            return True
        else:
            return False
    else:
        return False

# проверяет диагонали, одинаковые ли хотябы в одной из них все символы
def TestDiag(GF):
    if GF[1][1] != '-':
        if GF[0][0] == GF[1][1] and GF[0][0] == GF[2][2]:
            return True
        elif GF[2][0] == GF[1][1] and GF[2][0] == GF[0][2]:
            return True
        else:
            return False
    else:
        return False
    
# проверяет появилась ли выйгрышная позиция - три одинаковых символа
# в строке, столбце или по диагонали
def TestVictory(GF):
    Ret = False
    for Str in GF:
        if TestStr(Str):
            Ret = True
    for i in range(3):
        if TestCol(GF, i):
            Ret = True
    if not Ret:
        Ret = TestDiag(GF)
    return Ret

# осуществляет ход компьютера, возвращает True если ход удался
# возвращает False если компьютеру некуда ходить
def CompGo(GF):
    Go = False
    Res = False
    s = 0
    c = 0
    while not Go:
        if GF[s][c] == '-':
            GF[s][c] = '0'
            Go = True
            Res = True
        else:
            if c < 2:
                c += 1
            elif s < 2:
                c = 0
                s += 1
            else:
                Go = True
    return Res

# осуществляет ход игрока-пользователя
# возвращает координаты клетки, куда сходил пользователь
def movepl():
    List = [0,0]
    try:
        List[0] = int(input('Введите номер строки: '))
        List[1] = int(input('Введите номер столбца: '))
    except:
        print('Необходимо вводить числа от 1 до 3')
        return movepl()
    if 0 < List[0] < 4 and 0 < List[1] < 4:
        return List
    else:
        print('Необходимо вводить числа от 1 до 3')
        return movepl()
            
    
# создаем игровое поле
GameField = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]


print('---Игра крестики-нолики---')
print()
print('Это игрвое поле:')
# выводим пустое игровое поле на экран
show(GameField)

print('Вы хотите ходить первым или вторым? 1-первый, 2-второй')
a = input()
while a != '1' and a != '2':
    a = input('Введите 1 или 2: ')
    
# если пользователь выбрал ходить вторым, то делает ход компьютер
if a == '2':
    CompGo(GameField)
    print('Сходил компьютер:')
    show(GameField)
    
# запускаем игровой цикл
Game = True
while Game:
    # ходит игрок
    MovePlayer = movepl()
    # ставим крестик туда, куда сходил игрок
    GameField[MovePlayer[0]-1][MovePlayer[1]-1] = 'X'
    # выводим на экран игровое поле после хода игрока
    show(GameField)
    # проверяем не появилась выйгрышная позиция
    if TestVictory(GameField):
        print('Вы выйграли!')
        Game = False
    # если выйгрыша нет, то ходит компьютер
    elif CompGo(GameField):
        print('Comp go:')
        show(GameField)
        # проверяем не появилась выйгрышная позиция после хода компьютера
        if TestVictory(GameField):
            print('Вы проиграли!')
            Game = False
    else:
        # если компьютер не смог сходить и нет выйгрышной позиции, значит ничья
        print('Ничья')
        Game = False
        
    
