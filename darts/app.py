from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_quote_plus

from darts.models import db

app = Flask(__name__)
app.config.from_pyfile('app.config')
app.url_map.strict_slashes = False
app.jinja_env.filters['quote_plus'] = url_quote_plus

db.init_app(app)

from darts.views import *
