from header import *
from time import sleep
import os
from math import *
from datetime import date
from grovepi import *
from grove_rgb_lcd import *
import threading


MAX_RANGE = 1023 # maximum value for potentiometer


led = 4

button = 8
pot = 2
light_sensor = 1
rgb_led = 2
num_leds = 2

BRIGHT = 1
DIM = 0

brightness = BRIGHT

chainableRgbLed_init(rgb_led, num_leds)


pinMode(led, "OUTPUT")
pinMode(button, "INPUT")
threads = list()
sleep(1)


def get_level():
    l = analogRead(pot)
    if l > MAX_RANGE:
        l = MAX_RANGE
    return l

class ScrollThread(threading.Thread):
    def __init__(self, text, window_size = 32):
        super(ScrollThread, self).__init__()
        self._stop_event = threading.Event()
        self.text_arr = list(text + "                   ")
        self.win_size = window_size
        
    def stop(self):
        self._stop_event.set()

    def run(self):
        while(True):
            length = len(self.text_arr)
            for i in range(length):
                end = i + self.win_size
                if end > length:
                    end = length
                    window = self.text_arr[i:end]
                    window.extend(self.text_arr[:i+self.win_size-length])
                else:
                    window = self.text_arr[i:end]
                setText_norefresh("".join(window))
                time.sleep(0.3)
                if self._stop_event.is_set():
                    return


def get_light_level():
    return analogRead(light_sensor)


def disp_chore(numChores, day):
    """
    This function displays the chore on the lcd with the user's color.
    It also controls an led indicating whether the chore is completed or not
    :param chore: a tuple (chore name, user assigned to chore, completed or not, chore id)
    :return: none
    """
    if numChores == 0:
        setRGB(10, 10, 10)
        setText("There are no chores for today.")
        digitalWrite(led, 0)
        return
    ind = get_ind(get_level(), numChores)
    chore = day[ind]
    text = chore[0]
    if chore[2]:
        digitalWrite(led, 1)
    else:
        digitalWrite(led, 0)
    color = chore[1].color
    if not color in rgb_vals:
        color = "Red"
    setRGB(*rgb_vals[color][brightness])
    if len(threads) >= 1:
        old_thread = threads.pop()
        old_thread.stop()
        old_thread.join()
        sleep(0.1)
    if len(text) <= 32:
        setText_norefresh(text)
    else:
        t1 = ScrollThread(text)
        threads.append(t1)
        t1.start()


def get_cur_chore(day):
    num_chores = len(day)
    if num_chores == 0:
        return -1
    ind = get_ind(get_level(), num_chores)
    return day[ind]

    
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

def set_chores_done_led(user_name, led_num, day):
    if chores_complete(user_name, day):
        storeColor(*led_vals["Green"][brightness])
        chainableRgbLed_pattern(rgb_led, 0, led_num)
    else:
        storeColor(*led_vals["Red"][brightness])
        chainableRgbLed_pattern(rgb_led, 0, led_num)

        
days = get_days()
users = get_users()
old_mod_time = os.stat("app.db").st_mtime
today = date.today()

old_day_num = today.weekday()
day = days[today.weekday()]

old_level = get_level()
old_light_level = get_light_level()

old_chore = get_cur_chore(day)
disp_chore(len(day), day)

for i in range(len(users)):
    set_chores_done_led(users[i][0], users[i][3], old_day_num)
   
while True:
    today = date.today()
    today_num = today.weekday()
    new_mod_time = os.stat("app.db").st_mtime
    if new_mod_time != old_mod_time:
        # Get updated days list if file has been changed. Also
        # check if uodate to file caused a user's chore list
        # to be completed
        users = get_users()
        days = get_days()
        day = days[today.weekday()]
        for u in users:
            set_chores_done_led(u[0], u[3], today_num)

        disp_chore(len(day), day)
        old_mod_time = new_mod_time

    if old_day_num != today_num:
        day = days[today_num]

    num_chores = len(day)
    
    new_level = get_level()
    if abs(new_level - old_level) < 10:
        new_level = old_level
    else:
        old_level = new_level
    
    cur_chore = get_cur_chore(day)
    if digitalRead(button):
        """if button is pressed, flip the completed field of the
            current chore, then check if the chore list for that user
            is completed.
        """
        if cur_chore != -1:
            set_completed(cur_chore)
            set_chores_done_led(cur_chore[1].name, cur_chore[1].led, today_num)
        
    new_light_level = get_light_level()
    if new_light_level != old_light_level:
        if new_light_level < 90:
            if brightness != DIM:
                brightness = DIM
                disp_chore(len(day), day)
        else:
            if brightness != BRIGHT:
                brightness = BRIGHT
                disp_chore(len(day), day)
        for u in users:
            set_chores_done_led(u[0], u[3], today_num)
        old_light_level = new_light_level
        
    if num_chores > 0 and old_chore != cur_chore and cur_chore != -1:
        disp_chore(len(day), day)
        old_chore = cur_chore

chainableRgbLed_test(rgb_led, num_leds, 0)





