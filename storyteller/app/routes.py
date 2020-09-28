from app import app
from app.stories import _list_stories
from flask import request, render_template, Response

import pprint

@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def debug():
    str = pprint.pformat(request.environ, depth=5)
    return render_template('index.html')

@app.route('/debug')
def index():
    str = pprint.pformat(request.environ, depth=5)
    return Response(str, mimetype="text/text")


@app.route('/stories', methods=['GET'])
def get_stories():
    payload = _list_stories()
    return Response(payload, mimetype='application/json')
