import requests

response = requests.get('https://api.github.com')
data = response.json()
print(data)