#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import IFTTT_KEY
# ============== INTERNAL LIBRARIES
# ============== EXTERNAL LIBRARIES
from subprocess import Popen

def IFTTT(EVENT):
	url = 'https://maker.ifttt.com/trigger/' + EVENT + '/with/key/' + IFTTT_KEY
	Popen(['curl', '-X', 'POST', url])

def IFTTTcmd(EVENT):
	url = 'https://maker.ifttt.com/trigger/' + EVENT + '/with/key/' + IFTTT_KEY
	cmd = 'curl -X POST ' + url
	return cmd
