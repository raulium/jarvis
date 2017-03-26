#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import HOLIDAY_KEY
# ============== INTERNAL LIBRARIES
from web_mod import MyOpener
# ============== EXTERNAL LIBRARIES
from datetime import datetime, timedelta
import json, time

def getCurrentTime():
	hour = datetime.now().hour
	if hour > 12:
		hour = hour - 12
		tod = "PM"
	else:
		tod = "AM"
	min = datetime.now().minute
	if min < 10:
		min = "0" + str(min)
	return hour, min, tod

def snooze(new_alarm):
	newhour = int(new_alarm.split(':')[0])
	newmin = int(new_alarm.split(':')[1].split(' ')[0])
	newperiod = new_alarm.split(' ')[1]
	year = datetime.now().year
	month = datetime.now().month
	day = datetime.now().day

	if (newperiod == "PM"):
		newhour += 12

	wait = 1
	while wait > 0:
		time.sleep(wait)
		wait = int((datetime(year, month, day, newhour, newmin) - datetime.now()).total_seconds())

def thirty_min_before(time_string):
	h = int(time_string.split(':')[0])
	m = int(time_string.split(':')[1].split(' ')[0])
	t = time_string.split(' ')[1]
	year = datetime.now().year
	month = datetime.now().month
	day = datetime.now().day

	if (t == "PM"):
		if (h < 12):
			h += 12
	else:
		if (h == 12):
			h -= 12

	diff = datetime(year, month, day, h, m) - timedelta(minutes=30)
	print diff
	if diff.hour > 12:
		th = int(diff.hour) - 12
		tp = "PM"
	else:
		th = int(diff.hour)
		tp = "AM"
	new_string = str(th) + ':' + str(diff.minute) + " " + tp
	return new_string

def holidayDict():
	year = str(datetime.now().year)
	month = str(datetime.now().month)
	day = str(datetime.now().day)

	url = "https://holidayapi.com/v1/holidays?key=" + HOLIDAY_KEY +"&country=US&year=" + year + "&month=" + month + "&day=" + day

	agent = MyOpener()
	page = agent.open(url)

	jsonurl = page.read()
	data = json.loads(jsonurl)
	if len(data['holidays']) > 0:
		print(data)
		return str(data["holidays"][0]["name"])
	else:
		return None
