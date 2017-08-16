from flask import url_for, render_template, request, redirect, session
from darts.app import app
from darts.models import db, BBS_thread, BBS_posts
import darts.utils
import string
from sqlalchemy import or_
import datetime

# TODO: search feature
@app.route('/bbs', methods=['GET', 'POST'])
def bbs():
    if request.method == 'GET':
        num_threads_par_page = 10

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = max(0, int(page_id))

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''

        found_threads = BBS_thread.query.order_by(BBS_thread.created_at.desc()).filter(or_(BBS_thread.thread_title.contains(search_word), BBS_thread.thread_description.contains(search_word))).slice(page_id * 10, (page_id + 1) * 10).all()

        num_records = darts.utils.get_num_record_threads(search_word)

        thread_list = []
        for d in found_threads:
            thread_list.append((d.thread_id, d.thread_title, d.thread_description))

        num_page = int(max(0, num_records - 1) / num_threads_par_page) + 1

        pagination = {}
        pagination['current_page'] = page_id
        pagination['num_page'] = num_page

        return render_template('bbs.html', thread_list=thread_list, pagination=pagination, search_word=search_word)
    else:
        return render_template('bbs.html')

@app.route('/bbs/post', methods=['POST'])
def bbs_post():
    thread_id = request.form.get('thread_id')
    message = request.form.get('message')
    if thread_id is None:
        return redirect(url_for('bbs'))

    if not session.get('logged_in') or message == '':
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

        if thread_title == '':
            return redirect(url_for('bbs'))

        if not session.get('logged_in'):
            return redirect(url_for('bbs'))

        new_thread = BBS_thread(thread_title=thread_title, thread_description=thread_description, created_at=datetime.datetime.utcnow(), username=session['username'], ip_addr=request.environ['REMOTE_ADDR'])
        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('bbs'))

@app.route('/bbs/thread/<int:thread_id>', methods=['GET', 'POST'])
def bbs_view_thread(thread_id):
    if request.method == 'GET':
        num_threads_par_page = 10

        found_thread = BBS_thread.query.filter_by(thread_id=thread_id).first()
        if found_thread is None:
            return redirect(url_for('bbs'))

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = int(page_id)

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''

        found_posts = BBS_posts.query.filter(BBS_posts.message.contains(search_word)).filter_by(thread_id=thread_id).order_by(BBS_posts.posted_at.desc()).slice(page_id * num_threads_par_page, (page_id + 1) * num_threads_par_page).all()
        num_posts = db.session.query(BBS_posts).filter(BBS_posts.message.contains(search_word)).filter_by(thread_id=thread_id).count()

        post_list = []
        for d in found_posts:
            post_list.append((d.message, d.username, (d.posted_at + datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')))

        num_page = int(max(0, num_posts - 1) / num_threads_par_page) + 1

        pagination = {}
        pagination['current_page'] = page_id
        pagination['num_page'] = num_page

        return render_template('bbs_thread.html', post_list=post_list, thread_data=found_thread, pagination=pagination, search_word=search_word)
    else:
        return render_template('bbs_thread.html')
