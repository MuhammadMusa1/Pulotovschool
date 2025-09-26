# Определение функции без параметров
def greet():
    print("Hello, world!")

# Определение функции с параметром
def greet(name):
    print(f"Hello, {name}!")

# Определение функции с возвращаемым значением
def add(a, b):
    return a + b

# Вызов функций
greet()
greet("Alice")
result = add(3, 5)
print(result)  # выводит 8