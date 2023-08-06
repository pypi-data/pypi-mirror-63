# -*- encoding: utf-8 -*-

from flask.app import Flask
import sys
import hepdata_converter_ws
from hepdata_converter_ws import version

__author__ = 'Michał Szostak'

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object(hepdata_converter_ws)

    from hepdata_converter_ws.api import api
    app.register_blueprint(api)

    return app


def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        print "hepdata-converter-ws version %s" % version.__version__
        sys.exit()

    app = create_app()
    app.run(host='0.0.0.0')
