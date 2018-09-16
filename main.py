from header import *
from time import sleep
import os
from app import db
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

sleep(1)
greg = User("Greg", "blue")


def get_level():
    l = analogRead(pot)
    return l


def disp_chore(chore):
    """
    This function displays the chore on the lcd with the user's color.
    It also controls an led indicating whether the chore is completed or not
    :param chore: a tuple (chore name, user assigned to chore, completed or not, chore id)
    :return: none
    """
    color = chore[1].color.lower()
    #if chore completed column is true, turn on led
    if chore[2]:
        digitalWrite(led, 1)
    else:
        digitalWrite(led, 0)
    if not color in rgb_vals:
        color = "red"
    setRGB(*rgb_vals[color])
    setText(chore[0])


def get_ind(level, num_chore):
    """
    This function returns an index in the chore array given the level
    from potentiometer.
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


days = get_days()

old_mod_time = os.stat(DB_NAME).st_mtime
today = date.today()

old_day = today.weekday()
day = days[today.weekday()]# get the day for the day of week it is
old_level = get_level()
old_chore = ""
disp_chore(day[get_ind(old_level, len(day))])

while True:
    new_mod_time = os.stat(DB_NAME).st_mtime
    if new_mod_time != old_mod_time:
        days = get_days()
        old_mod_time = new_mod_time
    today = date.today()
    if old_day != today.weekday():
        day = days[today.weekday()]

    num_chores = len(day)
    
    new_level = get_level()
    if abs(new_level - old_level) < 10:
        new_level = old_level
    else:
        old_level = new_level
    ind = get_ind(new_level, num_chores)
    cur_chore = day[ind]

    if digitalRead(button):
        set_completed(cur_chore)
        disp_chore(day[ind])
        sleep(.3)
        
    # print("%s, %d, num_chores: %d" % (day.get_day(), today.weekday(), num_chores))
    if num_chores > 0 and old_chore != cur_chore:
        disp_chore(cur_chore)
        old_chore = cur_chore







