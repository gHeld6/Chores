from app.models import *
from time import sleep
import os
from math import *
from datetime import date
from grovepi import *
from grove_rgb_lcd import *
import threading
import datetime
import requests
import json


MAX_RANGE = 1023 # maximum value for potentiometer

"""
BRIGHT and DIM are used with rgb_vals and led_vals
to choose bright or dim versions of the colors.
"""
BRIGHT = 1
DIM = 0

record_file = "record.json"

TIMES = [(1, "1:00AM"), (2, "2:00AM"), (3, "3:00AM"), (4, "4:00AM"),
             (5, "5:00AM"), (6, "6:00AM"), (7, "7:00AM"), (8, "8:00AM"),
             (9, "9:00AM"), (10, "10:00AM"), (11, "11:00AM"), (12, "12:00PM"),
             (13, "1:00PM"), (14, "2:00PM"), (15, "3:00PM"), (16, "4:00PM"),
             (17, "5:00PM"), (18, "6:00PM"), (19, "7:00PM"), (20, "8:00PM"),
             (21, "9:00PM"), (22, "10:00PM"), (23, "11:00PM"), (24, "None")]
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
rgb_vals = {"Red": [[50, 0, 0],[255, 0, 0]], "Green": [[0, 50, 0],[0, 255, 0]],
            "Blue": [[0, 0, 50],[0, 0, 255]],
            "Purple": [[50, 0, 100],[255, 0, 255]]}
led_vals = {"Red":[[10, 0, 0],[50, 0, 0]], "Green": [[0, 10, 0], [0, 50, 0]]} 


def dt_to_min(dt):
    return int(dt.strftime("%H")) * 60 + int(dt.strftime("%M"))


def check_for_notify(now, notify_hour):
    if notify_hour == int(now.strftime("%H")) and now.strftime("%M") == "0":
        return True
    return False


def get_days():
    """
    This function returns a list of lists where each one represents a day of the week.
    Each inner list contains tuples for each chore for that day
    :return: List
    """
    days = [[], [], [], [], [], [], []]
    chores = Chore.query.order_by(Chore.day).all()
    for chore in chores:
        days[chore.day].append(
            {"chore": chore.chore, "user": User.query.filter_by(id=chore.user_id).first(),
             "complete": chore.completed, "id": chore.id, "notify_time": chore.time_completed_by,
             "recurring": chore.recurring})
    return days


def notify(name_str, body, title):
    tok = User.query.filter_by(name=name_str).first().token
    send_data = {"type": "note", "title": title, "body": body}
    response = requests.post("https://api.pushbullet.com/v2/pushes",
                             data=json.dumps(send_data),
                             headers={"Authorization": tok, "Content-Type": "application/json"})
    if response.status != 200:
        raise Exception("Failed to notify")


def remove_nonrecurring(day):
    for c in day:
        if not c["recurring"]:
            Chore.query.filter_by(id=c["id"]).delete()
    db.session.commit()
    
    
    
def get_users():
    """
    This function returns a list of tuples that represent each user
    :return: Array of tuples representing users:
             (user_name, user_color, user_id, user_led_number)
    """
    users_tup = []
    users = User.query.order_by(User.id).all()
    for user in users:
        users_tup.append((user.name, user.color, user.id, user.led, user.token))
    return users_tup


def set_completed(chore):
    """
    This function flips the completed value of the given chore
    :param chore: chore to to have completed field flipped
    :return: new completed value 
    """
    c = Chore.query.filter_by(id=chore["id"]).first()
    c.completed = not chore["complete"]
    db.session.commit()
    return c.completed


def set_chores_not_complete(day_num):
    chores = Chore.query.filter(Chore.day == day_num).all()
    for chore in chores:
        chore.completed = 0
    db.session.commit()


def chores_complete(name, day_num):
    """
    This function takes a user name and a day of the week and returns true
    if that user completed all their chores for that day.
    :param name: name of user to check if all chores are completed
    :param day: day to check if user completed chores
    :return: Boolean, whether or not user's chores are completed 
    """
    user = User.query.filter_by(name=name).first()
    u_id = user.id
    return len(Chore.query.filter(Chore.user_id == u_id, Chore.day == day_num, Chore.completed == 0).all()) == 0


def get_chore_counts(day):
    """

    """
    users = User.query.all()
    ret_val = []
    for u in users:
        num_chores = len(Chore.query.filter(Chore.user_id == u.id, Chore.day == int(day)).all())
        completed_chores = len(Chore.query.filter(Chore.user_id == u.id, Chore.day == int(day), Chore.completed == 1).all())
        ret_val.append({"name": u.name, "total_chores": num_chores, "chores_completed": completed_chores})
    return ret_val
    
    
