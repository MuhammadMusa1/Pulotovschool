import os

# Инициализация игрового поля
board = [[' ' for _ in range(3)] for _ in range(3)]

# Отрисовка игрового поля
def draw_board():
    os.system('cls' if os.name == 'nt' else 'clear')  # Очистка терминала
    print('  0 1 2')
    for i in range(3):
        print(f'{i} {"|".join(board[i])}')
        if i < 2:
            print('  -+-+-')

# Проверка победителя
def check_winner(player):
    # Проверка строк, столбцов и диагоналей
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Проверка на ничью
def is_board_full():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Основной игровой цикл
def main():
    players = ['X', 'O']
    current_player = 0

    print("Добро пожаловать в Крестики-Нолики!")
    print("Введите координаты хода в формате: строка столбец (например, '1 1')")
    
    while True:
        draw_board()
        print(f"Ход игрока {players[current_player]}")
        
        # Ввод хода
        try:
            row, col = map(int, input("Введите строку и столбец: ").split())
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Координаты должны быть от 0 до 2!")
                continue
            if board[row][col] != ' ':
                print("Эта клетка уже занята!")
                continue
        except ValueError:
            print("Неверный ввод! Введите два числа через пробел (например, '1 1').")
            continue

        # Установка хода
        board[row][col] = players[current_player]

        # Проверка победы
        if check_winner(players[current_player]):
            draw_board()
            print(f"Игрок {players[current_player]} победил!")
            break

        # Проверка ничьей
        if is_board_full():
            draw_board()
            print("Ничья!")
            break

        # Смена игрока
        current_player = (current_player + 1) % 2

if __name__ == "__main__":
    main()