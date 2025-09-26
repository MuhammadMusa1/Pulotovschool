import requests
from bs4 import BeautifulSoup

url = 'http://example.com'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

# Извлекаем все ссылки на странице
links = soup.find_all('a')
for link in links:
    print(link.get('href'))