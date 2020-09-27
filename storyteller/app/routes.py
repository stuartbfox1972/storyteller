from app import app
from flask import render_template, Response


@app.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def index():
    print request.__dict__
    #return render_template('index.html')


@app.route('/stories', methods=['GET'])
def get_stories():
    payload = _elasticache_flush()
    return Response(payload, mimetype='application/json')
