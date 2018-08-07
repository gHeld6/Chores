from Classes import Chore, User, Day, Week
import time
import random
from math import floor
from datetime import date

MAX_RANGE = 300 # maximum value for potentiometer


def get_level():
    return random.randint(0, 300)


def assign_chore(chore, user):
    chore.assign(user.get_name())


def disp_chore(chore):

    print("%s, %s, %s" % (chore.get_chore(), chore.who(), str(chore.is_completed())))


def get_ind(level, num_chore):
    """
    this function returns an index in the chore array given the level
    from potentiometer
    :param level: level reading from potentiometer
    :param num_chore: number of chores for the day
    :return: index for the list of chores
    """
    print(level)
    size = floor(MAX_RANGE / num_chore)
    r = size
    index = 0
    while r < level:
        r = size + r
        index = index + 1
    return index


if __name__ == '__main__':
    week = Week()
    greg = User("Greg")
    alex = User("Alex")

    c1 = Chore("Scoop cat litter", "greg")
    c2 = Chore("Scoop cat litter", "alex")
    c3 = Chore("Read to children", "alex")
    c4 = Chore("Do laundry", "greg")
    c4.set_completed("true")
    c1.set_completed("true")

    week.add_chore(c1, 1)
    week.add_chore(c2, 1)
    week.add_chore(c3, 1)
    week.add_chore(c4, 1)

    today = date.today()

    day = week.get_day(today.weekday())# get the day object for the day of week it is

    chores = day.get_chores()  # get list of chores for the day of week it is
    assign_chore(chores[0], alex)
    num_chores = day.get_num_chores()
    print("%s, %d, num_chores: %d" % (day.get_day(), today.weekday(), num_chores))
    for i in range(0, 3):
        if num_chores > 0:
            disp_chore(chores[get_ind(get_level(), num_chores)])














    '''for day in days:
        print(day.get_day())
        chores = day.get_chores()
        for c in chores:
            print("%s, Assigned to: %s" % (c.get_chore(), c.who()))
    '''






