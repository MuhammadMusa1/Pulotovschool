import requests

response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
data = response.json()

for key, value in data.items():
    print(f"{key}: {value}")