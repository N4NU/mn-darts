from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    score = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0


if __name__ == "__main__":
    from flask import Flask
    import os

    os.remove('darts/user.db')

    app = Flask(__name__)
    app.config.from_pyfile('app.config')

    db.init_app(app)
    db.create_all(app=app)
