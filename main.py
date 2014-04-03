import argparse
import os.path

from werkzeug.serving import run_simple

# TODO: config
_ROOT = os.path.abspath(os.path.dirname(__file__))

import timegrapple.app
import timegrapple.data
import timegrapple.views

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='grapple with time')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=5100)
    parser.add_argument('-r', '--reloader', default=False, action='store_true')

    args = parser.parse_args()

    run_simple(
        args.host, args.port, timegrapple.app.app, threaded=True,
        use_reloader=args.reloader, use_debugger=args.reloader,
        use_evalex=True)
