import requests
from bs4 import BeautifulSoup

url = 'https://lenta.ru/'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

# Извлекаем заголовки новостей
news_headlines = soup.find_all('h3', class_='card-mini__title')
print("Заголовки новостей:")
for headline in news_headlines:
    print(headline.text)