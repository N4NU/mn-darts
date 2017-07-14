"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///user.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SECRET_KEY = '26e03e82fb59fd88d5d7bb3ce5ab7680e9fc07a9d8c85d55'
)

db = SQLAlchemy(app)

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

db.create_all()

import darts.views