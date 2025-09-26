import requests
from bs4 import BeautifulSoup

# Загружаем страницу
url = 'http://example.com'
response = requests.get(url)
html = response.content

# Парсим HTML
soup = BeautifulSoup(html, 'html.parser')

# Извлекаем заголовок страницы
title = soup.title.string
print(f"Заголовок страницы: {title}")

# Извлекаем все ссылки на странице
links = soup.find_all('a')
print("Ссылки на странице:")
for link in links:
    print(link.get('href'))