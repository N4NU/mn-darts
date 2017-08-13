from darts.models import User
from darts.models import BBS_thread
import datetime

def get_ranking_list(start=0, stop=10):
    ranking_list = []
    for rank, user in enumerate(User.query.order_by(User.score).all()):
        ranking_list.append((rank + 1, user.username, user.score))
    return ranking_list[start:stop]

def get_threads_list(start=0, stop=10, fmt_str='%Y-%m-%d %H:%M:%S'):
    threads_list = []
    for thread in BBS_thread.query.order_by(BBS_thread.created_at.desc()).all():
        threads_list.append((thread.thread_id, thread.thread_title, thread.created_at.strftime(fmt_str)))
    return threads_list[start:stop]
