from flask import Flask, request, jsonify, Response
from os import getenv

app = Flask(__name__)

DATASET = {
    114: '514',
    810: '8931919',
    2017: 'https://blog.cal1.cn/post/RCTF%202017%20rCDN%20%26%20noxss%20writeup',
    2019: 'https://hackmd.io/IlzCicHXSN-MXl2JLCYr0g?view',
    2020: getenv('NOXSS_FLAG')
}


@app.before_request
def check_host():
    if request.host != getenv('NOXSS_HOST') or request.remote_addr != getenv('BOT_IP'):
        return Response(status=403)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/search")
def search_handler():
    keyword = request.args.get('keyword')
    if keyword is None:
        return jsonify(DATASET)
    else:
        ret = {}
        for i in DATASET:
            if keyword in DATASET[i]:
                ret[i] = DATASET[i]
        return jsonify(ret), 200 if len(ret) else 404


@app.after_request
def add_security_headers(resp):
    resp.headers['X-Frame-Options'] = 'sameorigin'
    resp.headers['Content-Security-Policy'] = 'default-src \'self\'; frame-src https://www.youtube.com'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'same-origin'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, )
