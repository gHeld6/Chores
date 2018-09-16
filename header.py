from app.models import *
file_name = "storage"
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
rgb_vals = {"Red": [255, 0, 0], "Green": [0, 255, 0], "Blue": [0, 0, 255],
            "Purple": [255, 0, 255]}


def get_days():
    """
    This function returns a list of lists where each one represents a day of the week.
    Each inner list contains tuples for each chore for that day
    :return:
    """
    days = [[], [], [], [], [], [], []]
    chores = Chore.query.order_by(Chore.day).all()
    for chore in chores:
        days[chore.day].append(
            (chore.chore, User.query.filter_by(id=chore.user_id).first(), chore.completed, chore.id))
    return days


def get_users():
    """
    This function returns a list of tuples that represent each user
    :return:
    """
    users_tup = []
    users = User.query.all()
    for user in users:
        users_tup.append((user.name, user.color, user.id))
    return users_tup


def set_completed(chore):
    """
    This function changes the completed of the given chore
    :param chore:
    :return:
    """
    c = Chore.query.filter_by(id=chore[3])
    c.completed = not chore[2]
    db.session.commit()