# Создание списка
fruits = ["apple", "banana", "cherry"]

# Доступ к элементам списка
print(fruits[0])  # выводит "apple"
print(fruits[1])  # выводит "banana"
print(fruits[2])  # выводит "cherry"

# Изменение элементов списка
fruits[1] = "blueberry"
print(fruits)  # выводит ["apple", "blueberry", "cherry"]

# Добавление элемента в список
fruits.append("orange")
print(fruits)  # выводит ["apple", "blueberry", "cherry", "orange"]

# Удаление элемента из списка
fruits.remove("blueberry")
print(fruits)  # выводит ["apple", "cherry", "orange"]