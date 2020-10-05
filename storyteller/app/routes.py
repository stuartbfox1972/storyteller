from app import app
from app.utils import _decode_token
from flask import render_template, request, Response, send_from_directory
from aws_xray_sdk.core import patch_all

patch_all()

@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    return Response("OK", mimetype='text/text')


@app.route('/api/v1.0/debug', methods=['GET'])
def api():
    #payload = _decode_token()
    #return render_template("debug.html", **variables)
    return Response('{"Message":"HELLO"}', mimetype='application/json')
