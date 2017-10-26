#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
from __future__ import print_function
import holidays
import time
from datetime import datetime, timedelta, date
# ============== INTERNAL LIBRARIES
# ============== CONFIG PARAMETERS
from config import MY_STATE


def getCurrentTime():
    hour = datetime.now().hour
    if hour > 12:
        hour = hour - 12
        tod = "PM"
    else:
        tod = "AM"
    m = datetime.now().minute
    if m < 10:
        m = "0" + str(m)
    return hour, m, tod


def getTime():
    hour, m, tod = getCurrentTime()
    myTime = str(hour) + ":" + str(m) + " " + str(tod)
    return myTime


def snooze(new_alarm):
    newhour = int(new_alarm.split(':')[0])
    newmin = int(new_alarm.split(':')[1].split(' ')[0])
    newperiod = new_alarm.split(' ')[1]
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    if newperiod == "PM":
        newhour += 12

    wait = 1
    while wait > 0:
        time.sleep(wait)
        wait = int((datetime(year, month, day, newhour, newmin) - datetime.now()).total_seconds())


def dto_to_string(MY_DTO):
    hour = MY_DTO.hour
    mins = MY_DTO.minute
    if hour > 12:
        return str(hour - 12) + ':' + str(mins) + " PM"
    else:
        return str(hour) + ':' + str(mins) + " AM"


def t_minus(time_string, minus):
    h = int(time_string.split(':')[0])
    m = int(time_string.split(':')[1].split(' ')[0])
    t = time_string.split(' ')[1]
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    if t == "PM":
        if h < 12:
            h += 12
    else:
        if h == 12:
            h -= 12

    diff = datetime(year, month, day, h, m) - timedelta(minutes=minus)
    print(diff)
    if diff.hour > 12:
        th = int(diff.hour) - 12
        tp = "PM"
    else:
        th = int(diff.hour)
        tp = "AM"
    new_string = str(th) + ':' + str(diff.minute) + " " + tp
    return new_string


def holidayDict():
    us_holidays = holidays.UnitedStates(state=MY_STATE)
    t = datetime.now().date()

    if t in us_holidays:
        return us_holidays.get(t)
    else:
        return None


def julianDate():
    return date.today().timetuple().tm_yday


def whatSeason(**keyword_parameters):
    """
	Returns integer 0-3 for the season of a given julian date, or current date if no
	julian is provided.
	0 = spring
	1 = summer
	2 = fall
	3 = winter
	"""
    JULIAN = julianDate()
    if 'julian' in keyword_parameters:
        JULIAN = keyword_parameters['julian']
    # "day of year" ranges for the northern hemisphere
    spring = range(80, 171)
    summer = range(172, 263)
    fall = range(264, 354)
    # winter = everything else
    if JULIAN in spring:
        return 0
    elif JULIAN in summer:
        return 1
    elif JULIAN in fall:
        return 2
    else:
        return 3
