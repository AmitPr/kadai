import time
from datetime import datetime

import dateparser
from blessings import Terminal


class Task:
    def __init__(self, value, date):
        self.value = value
        self.date = date

    def time_till_expire(self):
        return self.date - datetime.now()

    def __str__(self):
        return self.value + ' ' + str(self.time_till_expire())


class TaskManager:
    def __init__(self, term):
        self.term = term
        self.tasks = []
        self.selected = 0

    def update_tasks(self):
        print(self.term.move(0, 0), end='')
        if self.selected >= len(self.tasks):
            self.selected = self.selected % len(self.tasks)
        for i, t in enumerate(self.tasks):
            if i == self.selected:
                print(self.term.black_on_white(str(t)),
                      end=self.term.move_down)
            else:
                print(str(t), end=self.term.move_down)


if __name__ == "__main__":
    term = Terminal()
    with term.fullscreen():
        tm = TaskManager(term)
        for i in range(10):
            tm.tasks.append(
                Task("Test", dateparser.parse("in {0} hours".format(i))))
        while True:
            #   print(term.clear, end='')
            tm.update_tasks()
            tm.selected += 1
            time.sleep(.1)
            #tm.tasks.append(Task("Test", dateparser.parse(input())))
