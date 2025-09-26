import re

pattern = r"\d+"  # Одна или более цифр
text = "My number is 12345"
match = re.search(pattern, text)
if match:
    print("Найдено число:", match.group())