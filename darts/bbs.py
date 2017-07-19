from flask import url_for, render_template, request, redirect, session
from darts.app import app
from darts.models import db, BBS_thread
import string
from sqlalchemy import or_
import datetime

@app.route('/bbs', methods=['GET', 'POST'])
def bbs():
    if request.method == 'GET':
        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = int(page_id)

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''

        search_words = search_word.split()
        # found_threads = BBS_thread.query.order_by(BBS_thread.created_at.desc()).filter(or_(BBS_thread.thread_title.in_(search_words), BBS_thread.thread_description.in_(search_words))).slice(page_id * 10, (page_id + 1) * 10).all()
        found_threads = BBS_thread.query.order_by(BBS_thread.created_at.desc()).slice(page_id * 10, (page_id + 1) * 10).all()
        print(search_words)

        thread_list = []
        for d in found_threads:
            thread_list.append((d.thread_title, d.thread_description))
        return render_template('bbs.html', thread_list=thread_list)
    else:
        return render_template('bbs.html')

@app.route('/bbs/post', methods=['GET', 'POST'])
def bbs_post():
    if request.method == 'GET':
        return render_template('bbs.html')
    else:
        return render_template('bbs.html')

# TODO: CSRF
@app.route('/bbs/create', methods=['GET', 'POST'])
def bbs_create_thread():
    if request.method == 'GET':
        return render_template('bbs_create.html')
    else:
        thread_title = request.form.get('title')
        thread_description = request.form.get('description')

        new_thread = BBS_thread(thread_title=thread_title, thread_description=thread_description, created_at=datetime.datetime.utcnow())
        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('bbs'))
