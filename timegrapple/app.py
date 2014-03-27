import flask


app = flask.Flask('timegrapple')
app.config['SECRET_KEY'] = 'secret-sauce'
app.debug = True
