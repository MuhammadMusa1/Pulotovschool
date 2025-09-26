# Работа с множествами
fruits = {"apple", "banana", "cherry"}
fruits.add("orange")
fruits.remove("banana")
print(f"Фрукты: {fruits}")

# Работа со словарями
student = {
    "name": "Alice",
    "age": 21,
    "courses": ["Math", "CompSci"]
}
student["age"] = 22
student["grade"] = "A"
del student["courses"]
print(f"Студент: {student}")