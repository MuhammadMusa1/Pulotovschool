student = {
    "name": "Alice",
    "age": 21,
    "courses": ["Math", "CompSci"]
}

student["age"] = 22  # Изменение значения
print(student)

student["grade"] = "A"  # Добавление новой пары
print(student)

del student["courses"]  # Удаление пары
print(student)

print("name" in student)  # Проверка наличия ключа