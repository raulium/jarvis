#!/usr/local/env python

# ============== CONFIG PARAMETERS\
from config import DOW, NAME, SNOOZE_TIME, NORMAL_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import GREETING, WAKE, getReply, say, laboratoryOptions, volunteerOptions, dayOffOptions
from timing_mod import getCurrentTime, holidayDict, snooze, thirty_min_before, dto_to_string
from IFTTT_mod import IFTTT, IFTTTcmd
from lab_mod import labStatus
from mac_mod import setVolume, setDisplay, startMusic, ifMuted, openPage, ishome
from weather_mod import dailyReport, getSunsetDTO
from math_mod import fuckGreg
from yoga_mod import fuckGreg2
# ============== EXTERNAL LIBRARIES
import time, random
from datetime import datetime, timedelta
from subprocess import Popen
from atd import atd

def morningRoutine():
	"""Follow the mother-fucking routine, Donnie."""

	if ishome() is False:
	    return

	# if OVERRIDE:
	#     print "ABORTING!"
	#     return

	# ------------------------------------------------
	# CAUTION:  There is an "assumption" that the program is
	#           launching by crontab everyday at 7AM; so this could
	#           be problematic if, say, we were 12 hours off.
	#           The program does not check what the current time is
	#           as a condition to run -- it just runs.
	# ------------------------------------------------

	hour, min, tod = getCurrentTime()

	# ------------------------------------------------
	# Check if work is closed.
	# ------------------------------------------------

	WD = datetime.today().weekday()

	statusMessage = " "

	if WD >= 5:  # It's a weekend
		holString = holidayDict()
		if holString:
			statusMessage = "Happy " + holString + "! My gift to you was two hours of extra sleep."
		else:
			statusMessage = "Happy " + str(DOW[WD]) + "," + NAME + ". I hope you're satisfied with the extra sleep."
		snooze(thirty_min_before(SNOOZE_TIME))
		IFTTT("sunrise")
		snooze(SNOOZE_TIME)
	else:
		if labStatus(): # Where "True" or "1" means closed
			holString = holidayDict()
			if holString: #Today is a holiday
				statusMessage = "Happy " + holString + "! My gift to you was two hours of extra sleep."
			else:
				openPage("http://www.ll.mit.edu/status/index.html")
				statusMessage = "The laboratory appears to be closed today, so I took the liberty to let you sleep in.  I've opened the lab's status, if you care to learn more."
			snooze(thirty_min_before(SNOOZE_TIME))
			IFTTT("sunrise")
			snooze(SNOOZE_TIME)
		else:
			snooze(thirty_min_before(NORMAL_TIME))
			IFTTT("sunrise")
			snooze(NORMAL_TIME)

	# ------------------------------------------------
	# Time to start the show . . .
	# ------------------------------------------------

	setVolume(5)
	setDisplay()
	dailyReport()
	sunset = getSunsetDTO()
	l = IFTTTcmd('living_room_lifx')
	w = IFTTTcmd('living_room_wink')
	atd.at(l, sunset)
	atd.at(w, sunset)

	startMusic()
	time.sleep(30)

	hour = datetime.now().hour
	saytime = "The time is " + str(hour) + " o'clock " + tod + "."

	say(random.choice(GREETING) + ", " + NAME + ". " + saytime + " " + random.choice(WAKE))
	time.sleep(10)
	say(statusMessage)
	time.sleep(30)

	myStatus = 0
	if datetime.today().weekday() <= 4:
		myStatus = laboratoryOptions()
	elif datetime.today().weekday() == 5:
		myStatus = volunteerOptions()
	else:
		myStatus = dayOffOptions()

	# ------------------------------------------------
	# Otherwise, I'm already up. Give me the weather, Cecil!
	# ------------------------------------------------

	if myStatus < 1:
		fuckGreg()
		time.sleep(5)
		IFTTT("lights_on")
		IFTTT("wakeup")
		Popen(["afplay", "/tmp/DailyReport.aiff"])
		snooze(dto_to_string(datetime.now() + timedelta(minutes=50)))
		if ishome():
			IFTTT("wakeup")
			say("You will be late for work. You now have 20 minutes to depart.")
			snooze(dto_to_string(datetime.now() + timedelta(minutes=20)))
			if ishome():
				startMusic()
	else:
		say("Everything has been taken care of. Feel free to go back to bed.")

	# fuckGreg2()

	# SPECIAL_TIME = None

	# time.sleep(30)
	# while hour < 9:
	# 	if ifMuted():
	# 		setVolume(5)
	# 		say("Muting me isn't going to give you any more sleep, " + NAME + ".")
	# 	hour = datetime.now().hour
