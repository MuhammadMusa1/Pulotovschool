import requests

payload = {'username': 'student', 'password': 'password123'}
response = requests.post('https://httpbin.org/post', data=payload)
data = response.json()

print("Ответ от сервера:")
for key, value in data.items():
    print(f"{key}: {value}")