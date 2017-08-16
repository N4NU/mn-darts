from flask import url_for, render_template, request, redirect, session
from darts.app import app
from darts.models import Enquete_posts
import darts.utils

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
       session['is_admin'] = False 

    if request.method == 'GET':
        if session['is_admin']:
            num_threads_par_page = 10

            page_id = request.args.get('p')
            if page_id is None:
                page_id = 0
            else:
                page_id = max(0, int(page_id))

            search_word = request.args.get('q')
            if search_word is None:
                search_word = ''

            found_enquetes = Enquete_posts.query.order_by(Enquete_posts.posted_at.desc()).filter(Enquete_posts.message.contains(search_word)).slice(page_id * 10, (page_id + 1) * 10).all()

            num_records = darts.utils.get_num_record_threads(search_word)

            enquete_list = []
            for i, d in enumerate(found_enquetes):
                enquete_list.append((i + page_id * 10, d.service, d.message))

            num_page = int(max(0, num_records - 1) / num_threads_par_page) + 1

            pagination = {}
            pagination['current_page'] = page_id
            pagination['num_page'] = num_page

            return render_template('admin.html', enquete_list=enquete_list, pagination=pagination)
        else:
            return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        if session['is_admin']:
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if username == 'Fmqm3x5qjiLkXXo3q9HL' and password == '4ybVVu3yB3xDc8kEopHn':
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return 'Dont Login'