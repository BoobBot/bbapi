import os
import random
from functools import wraps

from flask import Flask, request, url_for, jsonify, render_template, abort, g
from gevent import monkey
import time
monkey.patch_all()
application = Flask(__name__)
application.config['PROPAGATE_EXCEPTIONS'] = False
keys = [
        ""
    ]


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Key') and request.headers.get('Key') in keys:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def random_image(cat):
    names = os.listdir(os.path.join('/var/www/bbapi/' + cat))
    random.shuffle(names)
    img_url = 'https://cdn.boob.bot/' + os.path.join(cat, random.choice(names))
    return img_url


@application.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/ping')
def ping():
    return jsonify(ping=g.request_time())


@application.route('/api/v2/cats')
def routes():
    names = os.listdir(os.path.join('/var/www/bbapi/'))
    return jsonify(names)


@application.route('/api/4k')
@require_appkey
def for_k():
    try:
        link = random_image('4k')
        return jsonify(url=link)
    except Exception as e:
        print(e)
        return jsonify(msg="404")


@application.route('/api/gif')
@require_appkey
def gif():
    try:
        link = random_image('gif')
        return jsonify(url=link)
    except Exception as e:
        print(e)
        return jsonify(msg="404")


@application.route('/api/pgif')
@require_appkey
def pgif():
    try:
        link = random_image('Pgif')
        return jsonify(url=link)
    except Exception as e:
        print(e)
        return jsonify(msg="404")


@application.route('/api/v2/img/<string:cat>')
@require_appkey
def new(cat):
    try:
        link = random_image(cat)
        return jsonify(url=link)
    except Exception as e:
        print(e)
        return jsonify(msg="404")


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5001)
