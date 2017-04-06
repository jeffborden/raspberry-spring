import requests

response = requests.get('https://httpbin.org/get')
data = response.json()
print(data)