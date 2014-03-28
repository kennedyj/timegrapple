from timegrapple.app import app
import flask
import json

from datetime import date

import timegrapple.data
from timegrapple.util import date_to_string, get_mondays


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


@app.route('/weeks/')
def get_week_list():
    return get_week_list_for(date.today().year)
    pass


@app.route('/weeks/<year>')
def get_week_list_for(year):
    days = [date_to_string(d) for d in get_mondays(int(year))]
    return flask.jsonify({'weeks': days})


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('error.html'), 404
