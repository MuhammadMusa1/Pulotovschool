import math
import random

# --- Константы ---
LEARNING_RATE = 0.1
EPOCHS = 10000

# --- Функции активации ---
def sigmoid(x):
    # Ограничиваем x, чтобы избежать переполнения
    x = max(-500, min(500, x))
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# --- Инициализация весов ---
# Вход: 2 нейрона (XOR имеет 2 входа)
# Скрытый слой: 4 нейрона
# Выход: 1 нейрон
random.seed(42)  # Для воспроизводимости

# Веса между входом и скрытым слоем: 2 входа → 4 нейрона
w1 = [[random.uniform(-1, 1) for _ in range(4)] for _ in range(2)]

# Веса между скрытым слоем и выходом: 4 нейрона → 1 выход
w2 = [random.uniform(-1, 1) for _ in range(4)]

# --- Данные для обучения (XOR) ---
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]  # Ожидаемые выходы

# --- Обучение ---
for epoch in range(EPOCHS):
    total_loss = 0
    for i in range(len(X)):
        # --- Прямой проход ---
        x = X[i]
        target = y[i]

        # Скрытый слой: 4 нейрона
        hidden = []
        for j in range(4):
            net = sum(x[k] * w1[k][j] for k in range(2))
            hidden.append(sigmoid(net))

        # Выходной слой
        output = sigmoid(sum(hidden[j] * w2[j] for j in range(4)))

        # --- Ошибка ---
        error = target - output
        total_loss += error ** 2

        # --- Обратное распространение ---
        # Градиент на выходе
        d_output = error * sigmoid_derivative(output)

        # Обновление весов между скрытым и выходом
        for j in range(4):
            w2[j] += LEARNING_RATE * d_output * hidden[j]

        # Обновление весов между входом и скрытым слоем
        for k in range(2):
            for j in range(4):
                d_hidden = d_output * w2[j] * sigmoid_derivative(hidden[j])
                w1[k][j] += LEARNING_RATE * d_hidden * x[k]

    # Печатаем прогресс каждые 1000 эпох
    if epoch % 1000 == 0:
        print(f"Эпоха {epoch}, ошибка: {total_loss:.6f}")

# --- Тестирование ---
print("\n--- Тестирование ---")
for i in range(len(X)):
    x = X[i]
    hidden = [sigmoid(sum(x[k] * w1[k][j] for k in range(2))) for j in range(4)]
    output = sigmoid(sum(hidden[j] * w2[j] for j in range(4)))
    print(f"Вход: {x} → Выход: {output:.4f} (ожидалось: {y[i]})")