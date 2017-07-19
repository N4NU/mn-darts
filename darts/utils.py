from darts.models import User

def get_ranking_list():
    ranking_list = []
    for rank, user in enumerate(User.query.order_by(User.score)):
        ranking_list.append((rank + 1, user.username, user.score))
    return ranking_list
