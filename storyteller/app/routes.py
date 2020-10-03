from app import app
from app.stories import _list_stories
from app.utils import _get_secret, _decode_token
from flask import request, render_template, Response, redirect, make_response

from aws_xray_sdk.core import patch_all

patch_all()

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


@app.route('/logout')
def logout():
    response = make_response(redirect(os.environ.get("LOGOUT_URL]", f"https://{request.host}/")))
    response.set_cookie("AWSELBAuthSessionCookie-0", "empty", max_age=-3600)

    return response


@app.route('/health')
def health():
    return Response("OK", mimetype='text/text')

@app.route('/api/v1.0/debug', methods=['GET'])
def api():
    variables = _decode_token()
    return render_template("debug.html", **variables)


@app.route('/api/v1.0/stories', methods=['GET'])
def get_stories():
    payload = _list_stories()
    return Response(payload, mimetype='application/json')
