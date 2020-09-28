from app import app
from app.stories import _list_stories
from app.utils import _get_secret, _decode_token
from flask import request, render_template, Response

import pprint

@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    str = pprint.pformat(request.headers, depth=5)
    secrets=_get_secret()
    str = secrets
    return Response(str, mimetype="text/html")


@app.route('/stories', methods=['GET'])
def get_stories():
    payload = _list_stories()
    return Response(payload, mimetype='application/json')


@app.route('/api', methods=['GET'])
def api():
    payload = request.headers
    return Response(str(payload), mimetype='application/json')