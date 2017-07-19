from flask import url_for, render_template, request, redirect, session
from darts.app import app
from darts.models import db, BBS_thread, BBS_posts
import string
from sqlalchemy import or_
import datetime

# TODO: search feature
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

        thread_list = []
        for d in found_threads:
            thread_list.append((d.thread_id, d.thread_title, d.thread_description))
        return render_template('bbs.html', thread_list=thread_list)
    else:
        return render_template('bbs.html')

@app.route('/bbs/post', methods=['POST'])
def bbs_post():
    thread_id = request.form.get('thread_id')
    message = request.form.get('message')
    if thread_id is None:
        return redirect(url_for('bbs'))

    if not session.get('logged_in') or message is None:
        return redirect(url_for('bbs_view_thread', thread_id=thread_id))

    new_post = BBS_posts(thread_id=thread_id, posted_at=datetime.datetime.utcnow(), username=session['username'], message=message, ip_addr=request.environ['REMOTE_ADDR'])
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('bbs_view_thread', thread_id=thread_id))

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

@app.route('/bbs/thread/<int:thread_id>', methods=['GET', 'POST'])
def bbs_view_thread(thread_id):
    thread_id
    if request.method == 'GET':

        found_thread = BBS_thread.query.filter_by(thread_id=thread_id).first()
        if found_thread is None:
            return redirect(url_for('bbs'))

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = int(page_id)

        found_posts = BBS_posts.query.filter_by(thread_id=thread_id).order_by(BBS_posts.posted_at.desc()).slice(page_id * 10, (page_id + 1) * 10).all()
        post_list = []
        for d in found_posts:
            post_list.append((d.message, d.username, (d.posted_at + datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')))
        return render_template('bbs_thread.html', post_list=post_list, thread_data=found_thread)
    else:
        return render_template('bbs_thread.html')
