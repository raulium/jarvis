#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import READING_TIME, BED_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import WARN, say, saiff
from timing_mod import getCurrentTime, snooze
from mac_mod import notification, setLivingRoom, setDisplay
from IFTTT_mod import IFTTT
# ============== EXTERNAL LIBRARIES
import time, random
from subprocess import Popen

def eveningRoutine():

	# if ishome() is False:
	#     return

	h, m, t = getCurrentTime()
	timeStr = str(h) + ":" + str(m) + " " + t
	TITLE = "Time Notification"
	MSG =  "It is " + timeStr + "."
	notification(TITLE, MSG)

	snooze("8:50 PM")

	h, m, t = getCurrentTime()
	timeStr = str(h) + ":" + str(m) + " " + t
	TITLE = "Time Notification"
	MSG =  "It is " + timeStr + "."
	notification(TITLE, MSG)

	rMSG = random.choice(WARN) + " It is " + timeStr + "."
	saiff(rMSG, "/tmp/BedTime.aiff")

	setLivingRoom()
	time.sleep(20)
	Popen(["afplay", "/tmp/BedTime.aiff"])
	time.sleep(10)
	setDisplay()

	notification(TITLE, "This computer will lock in 10 min.")
	snooze(READING_TIME)

	IFTTT("reading")

	snooze("9:55 PM")
	IFTTT("light_notice")
	snooze(BED_TIME)
	IFTTT("light_notice")
	IFTTT("sunset")
	IFTTT("lights_off")
