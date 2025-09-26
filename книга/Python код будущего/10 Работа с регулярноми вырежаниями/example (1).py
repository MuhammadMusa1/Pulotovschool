import re
pattern = r"hello"
text = "hello world"
match = re.search(pattern, text)
if match:
    print("Найдено:", match.group())