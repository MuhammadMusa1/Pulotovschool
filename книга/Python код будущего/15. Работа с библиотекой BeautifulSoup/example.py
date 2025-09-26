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
print(title)