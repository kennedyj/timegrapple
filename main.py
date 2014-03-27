import os.path

# TODO: config
_ROOT = os.path.abspath(os.path.dirname(__file__))

import timegrapple.app
import timegrapple.data
import timegrapple.views

if __name__ == '__main__':
    timegrapple.app.app.run()
