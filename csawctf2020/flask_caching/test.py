#!/usr/bin/env python3

from flask import Flask
from flask import request, redirect
from flask_caching import Cache
from redis import Redis
import jinja2
import os

app = Flask(__name__)
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['DEBUG'] = True

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
redis = Redis('localhost')
jinja_env = jinja2.Environment(autoescape=['html', 'xml'])


@app.route('/', methods=['GET', 'POST'])
def notes_post():
    if request.method == 'GET':
        return '''
        <h4>Post a note</h4>
        <form method=POST enctype=multipart/form-data>
        <input name=title placeholder=title>
        <input type=file name=content placeholder=content>
        <input type=submit>
        </form>
        '''

    print(request.form, flush=True)
    print(request.files, flush=True)
    title = request.form.get('title', default=None)
    content = request.files.get('content', default=None)

    if title is None or content is None:
        return 'Missing fields', 400

    content = content.stream.read()

    if len(title) > 100 or len(content) > 256:
        return 'Too long', 400

    redis.setex(name=title, value=content, time=10)  # Note will only live for max 30 seconds

    return 'Thanks!'


# This caching stuff is cool! Lets make a bunch of cached functions.
@cache.cached(timeout=3)
def _test0():
    return 'test'
@app.route('/test0')
def test0():
    _test0()
    return 'test'

# @cache.cached(timeout=3)
# @app.route('/test1')

# def test1():
#     return 'Cached for 50s'


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)
