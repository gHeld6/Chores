from app.models import *
file_name = "storage"
import app.models as m
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def get_days():
    """
    This function returns a list of lists where each one represents a day of the week.
    Each inner list contains tuples for each chore for that day
    :return:
    """
    days = [[], [], [], [], [], [], []]
    chores = m.Chore.query.order_by(m.Chore.day).all()
    for chore in chores:
        days[chore.day].append(
            (chore.chore, m.User.query.filter_by(id=chore.user_id).first(), chore.completed, chore.id))
    return days


def set_completed(chore):
    """
    This function changes the completed of the given chore
    :param chore:
    :return:
    """
    c = Chore.query.filter_by(id=chore[3])
    c.completed = not chore[2]
    db.session.commit()