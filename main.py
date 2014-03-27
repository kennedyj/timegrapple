import os.path
from werkzeug.serving import run_simple

# TODO: config
_ROOT = os.path.abspath(os.path.dirname(__file__))

import timegrapple.app
import timegrapple.data
import timegrapple.views

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5100
    run_simple(
        host, port, timegrapple.app.app, threaded=True,
        use_reloader=True, use_debugger=True, use_evalex=True)
