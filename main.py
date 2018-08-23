from Classes import *
import pickle
import time
import os
import random
from math import *
from datetime import date
from grovepi import *
from grove_rgb_lcd import *

MAX_RANGE = 1023 # maximum value for potentiometer


led = 4
button = 3
pot = 2

pinMode(led, "OUTPUT")
pinMode(button, "INPUT")

time.sleep(1)


rgb_vals = {"red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255],
            "purple": [255, 0, 255]}

def get_level():
    l = analogRead(pot)
    print str(l)
    return l

def assign_chore(chore, user):
    chore.assign(user.get_name())


def disp_chore(chore):
    color = chore.who().get_color()
    if chore.is_completed():
        digitalWrite(led, 1)
    else:
        digitalWrite(led, 0)
    setRGB(*rgb_vals[color])
    setText("%s" % chore.get_chore())


def get_ind(level, num_chore):
    """
    this function returns an index in the chore array given the level
    from potentiometer
    :param level: level reading from potentiometer
    :param num_chore: number of chores for the day
    :return: index for the list of chores
    """
    # print(level)
    size = floor(MAX_RANGE / num_chore) + 1
    r = size
    index = 0
    while r < level:
        r = size + r
        index = index + 1
    
    return index

def init_file():
    w = Week()
    with open(file_name, "rb") as file:
        pickle.dump(file, w)


#if storage file does not exist, create it and put an empty week in it
if not os.path.isfile(file_name):
    init_file()

week = get_week()

old_mod_time = os.stat(file_name).st_mtime
today = date.today()

old_day = today.weekday()
day = week.get_day(today.weekday())# get the day object for the day of week it is
chores = day.get_chores()  # get list of chores for the day of week it is
old_level = get_level()
disp_chore(chores[get_ind(old_level, len(chores))])

while True:
    new_mod_time = os.stat(file_name).st_mtime
    if new_mod_time != old_mod_time:
        week = get_week()
        old_mod_time = new_mod_time
    today = date.today()
    if old_day != today.weekday():
        day = week.get_day(today.weekday())  
        chores = day.get_chores()  # get list of chores for the day of week it is

    num_chores = len(chores)
    
    new_level = get_level()
    if abs(new_level - old_level) < 10:
        new_level = old_level
    else:
        old_level = new_level
    ind = get_ind(new_level, num_chores)
    cur_chore = chores[ind]

    if digitalRead(button):
        cur_chore.set_completed(not(cur_chore.is_completed()))
        disp_chore(chores[ind])
        update_file(week)
        time.sleep(.3)
        
    # print("%s, %d, num_chores: %d" % (day.get_day(), today.weekday(), num_chores))
    if num_chores > 0 and old_chore != cur_chore:
        disp_chore(cur_chore)
        old_chore = cur_chore







