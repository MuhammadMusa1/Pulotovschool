import re

# Поиск всех email-адресов
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
text = "My emails are test@example.com and hello@world.com."
matches = re.findall(pattern, text)
print("Email-адреса:", matches)