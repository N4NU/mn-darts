from flask import url_for, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import subprocess
from darts.app import app
from darts.models import db, User
import darts.utils 

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', threads_list=darts.utils.get_threads_list(0, 10), ranking_list=darts.utils.get_countup_ranking(0, 10))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            return render_template('login.html', login_failed=True)
        if bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', login_failed=True)

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
        user_data['barrel'] = found_user.barrel
        user_data['flight'] = found_user.flight
        user_data['shaft'] = found_user.shaft
        return render_template('user.html', user_data=user_data)

@app.route('/user/edit', methods=['GET', 'POST'])
def user_edit():
    if not session.get('logged_in'):
        session['logged_in'] = False
        return redirect(url_for('home'))

    if not session['logged_in']:
        return redirect(url_for('home'))

    found_user = User.query.filter_by(username=session['username']).first()
    if found_user is None:
        return render_template('user.html')
    else:
        user_data = {}
        user_data['username'] = found_user.username
        if request.method == 'POST':
            barrel = request.form['barrel']
            flight = request.form['flight']
            shaft = request.form['shaft']

            if barrel != '' and not barrel is None:
                found_user.barrel = barrel
                db.session.commit()

            if flight != '' and not flight is None:
                found_user.flight = flight
                db.session.commit()

            if shaft != '' and not shaft is None:
                found_user.shaft = shaft
                db.session.commit()

            return redirect(url_for('user', username=session['username']))
        else:
            return render_template('user_edit.html', user_data=user_data)

from darts.ranking import *
from darts.bbs import *
from darts.enquete import *
from darts.admin import *


