#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
from random import choice
from math import floor
from datetime import datetime
# ============== CONFIG PARAMETERS
from config import NAME
# ============== INTERNAL LIBRARIES
#?


def daysToWeekend():
    n = datetime.today().weekday()
    if n < 5:
        return 5 - n
    else:
        return 0


def counterString(i, unit):
    s = ["Only", "A mere", ""]
    e = ["more", "additional", ""]
    if i == 1:
        return choice(s) + " " + str(i) + " " + choice(e) + " " + unit + " until"
    else:
        return choice(s) + " " + str(i) + " " + choice(e) + " " + unit + "s until"


def weeksToDate(dto):
    n = datetime.today()
    return int(floor((dto - n).days / 7))


def motivate():
    c = ['You can do it.', "I have full confidence you'll make it.", "You'll be fine.", "Cease the day!",
         "You've got this.", "Don't forget to breathe.", "Just do it.", "Failure is not an option.",
         "Resistance is futile.", "Hang in there."]
    return choice(c)