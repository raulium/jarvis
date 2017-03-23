#!/usr/local/env python

# ============== CONFIG PARAMETERS
# ============== INTERNAL LIBRARIES
from timing_mod import snooze
from IFTTT_mod import IFTTT_mod
from mac_mod import openApp, setLivingRoom, startRadio, setVolume, setDisplay
# ============== EXTERNAL LIBRARIES

def vMorningRoutine():
	snooze(SNOOZE_TIME)
	# setLivingRoom()
	# startRadio()

def vEveningRoutine():
	snooze(READING_TIME)
	# closeApp("Google Chrome")
	IFTTT("reading")
	snooze(BED_TIME)
	IFTTT("sunset")
	IFTTT("lights_off")

def away():
	openApp("Google Chrome")
	setLivingRoom()
	startRadio()
	setVolume(5)
	setVolume(5)

def back():
	closeApp("Google Chrome")
	setDisplay()
