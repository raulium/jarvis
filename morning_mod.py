#!/usr/local/env python

# ============== CONFIG PARAMETERS\
from config import DOW, NAME, SNOOZE_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import GREETING, WAKE, getReply, say, UNFINISHED, laboratoryOptions, volunteerOptions, dayOffOptions
from timing_mod import getCurrentTime, holidayDict, snooze, thirty_min_before
from IFTTT_mod import IFTTT
from lab_mod import labStatus
from mac_mod import setVolume, setDisplay, startMusic, ifMuted, openPage
from weather_mod import dailyReport
from math_mod import fuckGreg
from yoga_mod import fuckGreg2
# ============== EXTERNAL LIBRARIES
import time
from datetime import datetime
from subprocess import Popen

def morningRoutine():
	"""Follow the mother-fucking routine, Donnie."""

	# if ishome() is False:
	#     return

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
	startMusic()
	time.sleep(30)

	hour = datetime.now().hour
	saytime = "The time is " + str(hour) + " o'clock " + tod + "."

	say(random.choice(GREETING) + ", " + NAME + ". " + saytime + " " + random.choice(WAKE))
	time.sleep(10)
	say(statusMessage)
	time.sleep(30)

	# ------------------------------------------------
	# Ask three times if I'm awake.  Missinterpretation isn't
	# counted as an iteration.
	# ------------------------------------------------

	# i = 0
	# while i < 3:
	# 	say("Are you awake?")
	# 	reply = getReply()
	# 	if reply is "ERR":
	# 		say("I'm sorry, I didn't quite catch that.")
	# 		time.sleep(2.5)
	# 	elif reply is "NULL":
	# 		say(NAME + " " + random.choice(LAZY))
	# 		time.sleep(3)
	# 		awake = 0
	# 		i += 1
	# 	else:
	# 		say(random.choice(POSITIVE))
	# 		time.sleep(2)
	# 		awake = 1
	# 		i = 3

    if datetime.date.weekday() <= 4:
        laboratoryOptions()
    elif datetime.date.weekday() == 5:
        volunteerOptions()
    else:
        dayOffOptions()


	# ------------------------------------------------
	# If I'm not awake, you are authorized to be annoying...
	# ------------------------------------------------

	# if awake == 0:
	# 	time.sleep(2)
	# 	say(random.choice(UNFINISHED) + ", I can't be certain if you're awake yet.  So if you haven't turned off the music, I'm going to turn it up now.")
	# 	time.sleep(10)
	# 	setVolume(10)
	# 	time.sleep(600)

	# ------------------------------------------------
	# Otherwise, I'm already up. Give me the weather, Cecil!
	# ------------------------------------------------

	fuckGreg()
	fuckGreg2()

	time.sleep(5)
	IFTTT("lights_on")
	Popen(["afplay", "/tmp/DailyReport.aiff"])

	SPECIAL_TIME = None

	time.sleep(30)
	while hour < 9:
		if ifMuted():
			setVolume(5)
			say("Muting me isn't going to give you any more sleep, " + NAME + ".")
		hour = datetime.now().hour
