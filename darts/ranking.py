from flask import url_for, render_template, request, redirect, session
from darts.app import app
import darts.utils
from darts.models import db, Score_countup, Score_501, Score_cricket
import datetime

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():

    ranking_countup_list = darts.utils.get_countup_ranking()
    ranking_501_list = darts.utils.get_501_ranking()
    ranking_cricket_list = darts.utils.get_cricket_ranking()

    return render_template('ranking.html', ranking_countup_list=ranking_countup_list, ranking_501_list=ranking_501_list, ranking_cricket_list=ranking_cricket_list)

@app.route('/ranking/countup', methods=['GET', 'POST'])
def ranking_countup():
    if request.method == 'GET':
        num_ranking_par_page = 10

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = max(0, int(page_id))

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''

        ranking_countup_list = darts.utils.get_countup_ranking(offset=page_id * num_ranking_par_page, limit=(page_id + 1) * num_ranking_par_page, search_word=search_word)
        num_records = darts.utils.get_num_record_countup_ranking(search_word=search_word)

        num_page = int(max(0, num_records - 1) / num_ranking_par_page) + 1

        pagination = {}
        pagination['current_page'] = page_id
        pagination['num_page'] = num_page

        return render_template('ranking_countup.html', ranking_countup_list=ranking_countup_list, pagination=pagination, search_word=search_word)
    else:
        return render_template('ranking_countup.html')

@app.route('/ranking/countup/post', methods=['GET', 'POST'])
def ranking_countup_post():
    if request.method == 'GET':
        return render_template('ranking_countup_post.html')
    else:
        round_data = request.form.get('round_data')

        if round_data == '':
            return redirect(url_for('ranking_countup_post'))

        if not session.get('logged_in'):
            return redirect(url_for('ranking_countup_post'))

        l = list(map(int, round_data.split(',')))
        score = 0
        for i in range(0, len(l), 2):
            score += l[i] * l[i + 1]

        new_score = Score_countup(posted_at=datetime.datetime.utcnow(), username=session['username'], round_data=round_data, score=score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('ranking_countup'))

@app.route('/ranking/501', methods=['GET', 'POST'])
def ranking_501():
    if request.method == 'GET':
        num_ranking_par_page = 10

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = max(0, int(page_id))

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''

        ranking_501_list = darts.utils.get_501_ranking(offset=page_id * num_ranking_par_page, limit=(page_id + 1) * num_ranking_par_page)
        num_records = darts.utils.get_num_record_501_ranking(search_word=search_word)

        num_page = int(max(0, num_records - 1) / num_ranking_par_page) + 1

        pagination = {}
        pagination['current_page'] = page_id
        pagination['num_page'] = num_page

        return render_template('ranking_501.html', ranking_501_list=ranking_501_list, pagination=pagination)
    else:
        return render_template('ranking_501.html')

@app.route('/ranking/501/post', methods=['GET', 'POST'])
def ranking_501_post():
    if request.method == 'GET':
        return render_template('ranking_501_post.html')
    else:
        round_data = request.form.get('round_data')

        if round_data == '':
            return redirect(url_for('ranking_501_post'))

        if not session.get('logged_in'):
            return redirect(url_for('ranking_501_post'))

        l = list(map(int, round_data.split(',')))
        score = 0
        remain_score = 501
        for i in range(0, len(l), 2):
            dart_score = l[i] * l[i + 1]
            if remain_score - dart_score > 0:
                remain_score -= dart_score
            elif remain_score - dart_score == 0:
                remain_score -= dart_score
                break

        score = i / 2 + 1

        new_score = Score_501(posted_at=datetime.datetime.utcnow(), username=session['username'], round_data=round_data, score=score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('ranking_501'))

@app.route('/ranking/cricket', methods=['GET', 'POST'])
def ranking_cricket():
    if request.method == 'GET':
        num_ranking_par_page = 10

        page_id = request.args.get('p')
        if page_id is None:
            page_id = 0
        else:
            page_id = max(0, int(page_id))

        search_word = request.args.get('q')
        if search_word is None:
            search_word = ''
        
        ranking_cricket_list = darts.utils.get_cricket_ranking(offset=page_id * num_ranking_par_page, limit=(page_id + 1) * num_ranking_par_page)
        num_records = darts.utils.get_num_record_cricket_ranking(search_word=search_word)

        num_page = int(max(0, num_records - 1) / num_ranking_par_page) + 1

        pagination = {}
        pagination['current_page'] = page_id
        pagination['num_page'] = num_page

        return render_template('ranking_cricket.html', ranking_cricket_list=ranking_cricket_list, pagination=pagination)
    else:
        return render_template('ranking_cricket.html')

@app.route('/ranking/cricket/post', methods=['GET', 'POST'])
def ranking_cricket_post():
    if request.method == 'GET':
        return render_template('ranking_cricket_post.html')
    else:
        round_data = request.form.get('round_data')

        if round_data == '':
            return redirect(url_for('ranking_cricket_post'))

        if not session.get('logged_in'):
            return redirect(url_for('ranking_cricket_post'))

        l = list(map(int, round_data.split(',')))
        score = 0
        remain_score = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:3, 16:3, 17:3, 18:3, 19:3, 20:3, 25:3}
        for i in range(0, len(l), 2):
            remain_score[l[i]] -= l[i + 1]
            if all(map(lambda x: x <= 0, remain_score.values())):
                break

        score = i / 2 + 1

        new_score = Score_cricket(posted_at=datetime.datetime.utcnow(), username=session['username'], round_data=round_data, score=score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('ranking_cricket'))
