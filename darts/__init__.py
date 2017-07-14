"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///user.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SECRET_KEY = '26e03e82fb59fd88d5d7bb3ce5ab7680e9fc07a9d8c85d55'
)

import darts.views