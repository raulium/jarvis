#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import SNOOZE_TIME, READING_TIME, BED_TIME
# ============== INTERNAL LIBRARIES
from timing_mod import snooze
from IFTTT_mod import IFTTT
from mac_mod import openApp, setLivingRoom, startRadio, setVolume, setDisplay, macTerm
# ============== EXTERNAL LIBRARIES
import os.path

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
	if not checkAwayStatus():
		cmd = ['touch', '/tmp/away.lock']
		macTerm(cmd)
		# setLivingRoom()
		# setVolume(5)

def back():
	if checkAwayStatus():
		cmd = ['rm', '/tmp/away.lock']
		macTerm(cmd)
		# setDisplay()

def checkAwayStatus():
	result = os.path.exists('/tmp/away.lock')
	return result;

def setVacation():
	cmd = ['touch', '/tmp/vacation.lock']
	macTerm(cmd)

def rmVacation():
	cmd = ['rm', '/tmp/vacation.lock']
	macTerm(cmd)

def checkVacationStatus():
	result = os.path.exists('/tmp/vacation.lock')
	return result;
