import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder


__version__ = '0.1.0'


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

from . import views
