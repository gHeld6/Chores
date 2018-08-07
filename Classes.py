class Chore:

    def __init__(self, chore, user):
        self.chore = chore
        self.done = False
        self.assigned_to = str(user).title()

    def is_completed(self):
        """
        returns whether or not the chore is done
        :return:
        """
        return self.done

    def assign(self, user):
        self.assigned_to = user

    def who(self):
        return self.assigned_to

    def get_chore(self):
        return self.chore

    def set_completed(self, val):
        if str(val).lower() == "true":
            self.done = True
        else:
            self.done = False


class User:

    def __init__(self, name) -> None:
        self.name = str(name).title()
        self.num_chores = 0

    def chores_assigned(self) -> int:
        return self.num_chores

    def add_chore(self, chore):
        self.num_chores += 1

    def get_name(self):
        return self.name


class Day():

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, day_num):
        self.day = day_num
        self.chore_list = []

    def add_chore(self, chore):
        self.chore_list.append(chore)

    def get_day(self):
        return self.days[self.day]

    def get_chores(self):
        return self.chore_list.copy()

    def get_num_chores(self):
        return len(self.chore_list)


class Week:

    def __init__(self):
        self.day_list = [Day(0), Day(1), Day(2), Day(3), Day(4), Day(5), Day(6)]

    def add_chore(self, chore, day):
        self.day_list[int(day)].add_chore(chore)

    def get_day(self, day):
        return self.day_list[int(day)]

    def get_days(self):
        return self.day_list.copy()