from timegrapple.app import app
import flask
import json

import timegrapple.data


@app.route('/')
def root():
    return app.send_static_file('views/index.html')


@app.route('/sheets/', methods=['GET'])
def today():
    return flask.jsonify(timegrapple.data.load())


@app.route('/sheets/<when>', methods=['GET'])
def for_day(when):
    return flask.jsonify(timegrapple.data.load(when))


@app.route('/sheets/<when>', methods=['POST'])
def for_day_save(when):
    data = json.loads(flask.request.data)

    timegrapple.data.save(when, data)
    return "saved", 200


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('error.html'), 404
