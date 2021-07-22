import requests
from base64 import b64decode, b64encode


# token for name: king-horse-5diuoe7tpxjen8xu0n8
token = 'pFdnRfIh2G6G1bqJSPzChmImAQo2DJ/gsJcoDi441CDVUy0pJZpAkmvCoJA9F7fjaghUp3dTymR1bA=='

token_buffer = bytearray(b64decode(token))

def try_char(i):
    
    token_buffer[12+29] = i

    b = b64encode(token_buffer).decode()

    r = requests.get('https://app.maria-bin.tk/new', headers={
        'Cookie': '__Host-token='+ b
    })
    print(r.text)


for i in range(0,255):
    try_char(i)