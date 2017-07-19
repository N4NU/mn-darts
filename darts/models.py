from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0

class BBS_thread(db.Model):
    thread_id = db.Column(db.Integer, primary_key=True)
    thread_title = db.Column(db.Unicode(100), nullable=False)
    thread_description = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, thread_title, thread_description, created_at):
        self.thread_title = thread_title
        self.thread_description = thread_description
        self.created_at = created_at

class BBS_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_name = db.Column(db.Unicode(20), nullable=False)
    message = db.Column(db.UnicodeText, nullable=False)
    ip_addr = db.Column(db.String(16), nullable=False)

    def __init__(self, thread_id, posted_at, user_name, message, ip_addr):
        self.thread_id = thread_id
        self.posted_at = posted_at
        self.user_name = user_name
        self.message = message
        self.ip_addr = ip_addr

if __name__ == "__main__":
    from flask import Flask
    import os

    os.remove('darts/user.db')

    app = Flask(__name__)
    app.config.from_pyfile('app.config')

    db.init_app(app)
    db.create_all(app=app)
