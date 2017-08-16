from darts.models import db
from darts.models import User
from darts.models import BBS_thread
from darts.models import Score_countup
from darts.models import Score_501
from darts.models import Score_cricket
import datetime
from sqlalchemy import or_

def get_ranking_list(offset=0, limit=10):
    ranking_list = []
    for rank, user in enumerate(User.query.order_by(User.score).slice(offset, limit).all()):
        ranking_list.append((rank + 1, user.username, user.score))
    return ranking_list

def get_threads_list(offset=0, limit=10, fmt_str='%Y-%m-%d %H:%M:%S'):
    threads_list = []
    for thread in BBS_thread.query.order_by(BBS_thread.created_at.desc()).slice(offset, limit).all():
        threads_list.append((thread.thread_id, thread.thread_title, (thread.created_at + datetime.timedelta(hours=9)).strftime(fmt_str)))
    return threads_list

def get_num_record_threads(search_word=''):
    return db.session.query(BBS_thread).filter(or_(BBS_thread.thread_title.contains(search_word), BBS_thread.thread_description.contains(search_word))).count()

def get_countup_ranking(offset=0, limit=10, search_word=''):
    ranking_list = []
    for rank, score in enumerate(Score_countup.query.filter(Score_countup.username.contains(search_word)).order_by(Score_countup.score.desc()).slice(offset, limit).all()):
        ranking_list.append((offset + rank + 1, score.username, score.score))
    return ranking_list

def get_num_record_countup_ranking(search_word=''):
    return db.session.query(Score_countup).filter(Score_countup.username.contains(search_word)).count()

def get_501_ranking(offset=0, limit=10, search_word=''):
    ranking_list = []
    for rank, score in enumerate(Score_501.query.filter(Score_501.username.contains(search_word)).order_by(Score_501.score).slice(offset, limit).all()):
        ranking_list.append((offset + rank + 1, score.username, score.score))
    return ranking_list

def get_num_record_501_ranking(search_word=''):
    return db.session.query(Score_501).filter(Score_501.username.contains(search_word)).count()

def get_cricket_ranking(offset=0, limit=10, search_word=''):
    ranking_list = []
    for rank, score in enumerate(Score_cricket.query.filter(Score_cricket.username.contains(search_word)).order_by(Score_cricket.score).slice(offset, limit).all()):
        ranking_list.append((offset + rank + 1, score.username, score.score))
    return ranking_list

def get_num_record_cricket_ranking(search_word=''):
    return db.session.query(Score_cricket).filter(Score_cricket.username.contains(search_word)).count()
