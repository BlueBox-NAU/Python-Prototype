import requests

request = requests.post('http://127.0.0.1:5500/test/1/2', json = {'num1': 3, 'num2': 4})

print(request.text)