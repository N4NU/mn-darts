from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from darts.models import db

app = Flask(__name__)
app.config.from_pyfile('app.config')

db.init_app(app)

from darts.views import *
