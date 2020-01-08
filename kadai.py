import time
from datetime import datetime
import math
import sys

import dateparser
from blessed import Terminal
title = '''    ,,,,,,,,,,

   ▐██████████▌  ▐██████████████████▌       ██████████████  █████████████████▌
    ``````````   ▐███▀""╙▀███M""╙███▌       ███▌`````▐████  ``````▐███▀```````
 ▐█████████████H ▐███▌,,,║██▌,,,╓███▌       ████▓▓▓▓▓█████   ▄▄▄▄▄████▄▄▄▄▄▄▄
 ╙▀▀▀▀▀▀▀▀▀▀▀▀▀╩ ▐██████████████████▌       ███▀"""""╙████   ║███▀▀▀▀▀▀▀▀███▌
   ,,,,,,,,,,,,  ▐███▌```║██▌"``"███▌       ████▄▄▄▄▄▄████   ║██▌,,,,,,,▄███▌
   ▐██████████▌  ▐███▄╓╓╓▄███▄╓╓▄███▌       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀   ║██████████████▌
    ``````````   ▐██████████████████▌                        ║██▌       ▐███▌
   ╔▄▄▄▄▄▄▄▄▄▄▄   ```````████M``````      ▓████████████████M ║██████████████▌
   ║██████████▌ ╓▄▄▄▄▄▄▄▄████▓▄▄▄▄▄▄▄▄    ╙╜╜╜╜╜╜▀███▀╜╜╜╜╜^ ║██▌```````▐███▌
                ▐█████████████████████      ▄▄▄  ▐███        ║███▌▄▄▄▄▄▄▓███▌
   ▐██████████▌  `````╠████████▌           ▐███  ▐████████▌  ╝▀▀▀▀▀▀▀▀▀▀▀▀▀▀╧
   ▐███╨╙╙╙███▌     ,▄███████████▄         ║███▄ ▐███▀╜╜╜╜╜   ╓▄██▄⌐  τ▓██▄,
   ▐██▌    ║██▌   ╓▄████╙████M╙████▄       ║████▄▄██▌     ,╓▄████▀      ╙████▄
   ▐██▌w╓╓╓███▌╓▄█████╜  ║███  `▀████▄,   ╓███▀██████,     "▀█▀`          ╙▀▀"
   ▐██████████▌`▀███╨    ║███    `▀██╩   ╓███▀  "▀████████▓▓▄▄▄▄▄▄▄▄▄▄▄▄▄▓▓▄▓▓Γ
   ║██▌```````   ``      ║███      `      ╙█▀       `╙╙▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  '''
def pretty_date(time):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    diff = time-now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "now"
        if second_diff < 60:
            return "in " + str(second_diff) + " seconds"
        if second_diff < 120:
            return "in a minute"
        if second_diff < 3600:
            return "in " + str(math.floor(second_diff / 60)) + " minutes"
        if second_diff < 7200:
            return "in an hour"
        if second_diff < 86400:
            return "in " + str(math.floor(second_diff / 3600)) + " hours"
    if day_diff == 1:
        return "Tomorrow"
    if day_diff < 7:
        return "in " + str(math.floor(day_diff)) + " days"
    if day_diff < 31:
        return "in " + str(math.floor(day_diff / 7)) + " weeks"
    if day_diff < 365:
        return "in " + str(math.floor(day_diff / 30)) + " months"
    return "in " + str(math.floor(day_diff / 365)) + " years"
class Task:
    def __init__(self, value, date):
        self.value = value
        self.date = date

    def time_till_expire(self):
        return self.date - datetime.now()

    def __str__(self):
        return self.value + ' ' + pretty_date(self.date)


class TaskManager:
    def __init__(self, term):
        self.term = term
        self.tasks = []
        self.selected = 0

    def update_tasks(self):
        print(self.term.move(0, 0), end='')
        if self.selected >= len(self.tasks) or self.selected < 0:
            self.selected = self.selected % len(self.tasks)
        for i, t in enumerate(self.tasks):
            print(self.term.color(5)(str(i+1)+'. '),end='\t')
            if i == self.selected:
                print(self.term.black_on_white(str(t)),
                      end=self.term.move_down)
            else:
                print(str(t), end=self.term.move_down)


if __name__ == "__main__":
    term = Terminal()
    tm = TaskManager(term)
    with term.fullscreen():
        for i in range(0,10):
            tm.tasks.append(
                Task("Test", dateparser.parse("in {0} minutes".format(i))))
    while True:
        with term.fullscreen(),term.cbreak():
            tm.update_tasks()
            inp = term.inkey(timeout=1)
            raw = repr(inp).replace("'","")
            if not inp:
                pass
            elif raw == u'KEY_UP':
                tm.selected -= 1
            elif raw == u'KEY_DOWN':
                tm.selected += 1
            elif raw in (u'q', u'Q'):
                sys.exit()
