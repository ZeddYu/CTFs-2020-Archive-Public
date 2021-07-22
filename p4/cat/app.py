from flask import Flask, request, render_template
import os
import json
import datetime
import hashlib
import random
import os
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/cats')
def list_cats():
    path = request.args.get('kind')
    if not path:
        return ''
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    try:
        files = list(filter(lambda x : x != 'bot', os.listdir('./static/'+path)))
        response = f'{{"status": "ok", "content": {json.dumps(files)}}}'
        return response, 200, headers
    except Exception as e:
        print(e)
        return f'{{"status": "error", "content": "{path} could not be found"}}', 200, headers

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        captcha = request.form.get('captcha')
        if not captcha:
            return 'plz gimme me some coptcha :('
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': os.environ.get('RECAPTCHA_SECRET'), 'response': captcha})
        if response.json()['success'] != True:
            return 'coptcha failed :('
        url = request.form.get('url', '')

        filename = datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S") + hashlib.md5(
            (url + str(random.randint(0, 0xffffffff))).encode('utf-8')).hexdigest()
        with open('bot/bot_stuff/{}'.format(filename), 'w') as f:
            f.write(url)
        return 'reported'
    return render_template('report.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run()