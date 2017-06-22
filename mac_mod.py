#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import BASE_PATH, EMAIL, ICLOUD, IPHONE_ID, HOME_COORD, USERNAME
# ============== INTERNAL LIBRARIES
# ============== EXTERNAL LIBRARIES
import time
from subprocess import Popen, os, PIPE
from pyicloud import PyiCloudService


def iCloudConnect():
    api = PyiCloudService(EMAIL)
    if api.requires_2fa:
        import click
        print "Two-factor authentication required. Your trusted devices are:"

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print "  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber')))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print "Failed to send verification code"
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print "Failed to verify verification code"
            sys.exit(1)


def macTerm(CMD):
    runcmd = ['sudo', '-u', USERNAME] + CMD
    Popen( runcmd )


def appleScript(CMD):
    c = ['osascript', '-e'] + CMD
    macTerm(c)


def setVolume(VALUE):
    '''
    ... for an ungodly reason, Apple has made it such that the volume scale
    is from 0 - 7. And real numbers. Meaning 3.5 is the center of the scale.
    ... w... t... f...
    '''
    cmd = ['osascript', '-e', 'set Volume ' + str(VALUE)]
    macTerm(cmd)


def setLivingRoom():
    """ Set Audio Output to Living Room. """
    setVolume(7)
    cmd = [BASE_PATH + 'AppleScripts/audioLivingRoom.applescript']
    macTerm(cmd)
    time.sleep(1)


def setDisplay():
    """ Set Audio Output to Cinema Display. """
    setVolume(4)
    cmd = [BASE_PATH + 'AppleScripts/audioDisplay.applescript']
    macTerm(cmd)
    time.sleep(1)


# THIS DOESN'T APPEAR TO WORK... INVESTIGATE
# def lockScreen():
#     """Lock the screen"""
#     Popen(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'])


def notification(TITLE, MSG):
    """ Send notification to Notificaiton Center. """
    cmd = ['osascript', '-e', "display notification " + '"' + MSG + '"' + " with title " + '"' + TITLE +'" sound name "Hero"']
    macTerm(cmd)


def ifMuted():
    out, err = Popen(['osascript', '-e', 'get volume settings'], stdout=PIPE ).communicate()
    l = out.split(',')
    if 'true' in str(l[3]):
        return 1
    else:
        return 0


# STOPPED WORKING -- FIX THIS
def startRadio():
    openPage("http://www.wgbh.org/audioPlayers/wgbh.cfm")


def startMusic():
    closeApp('Spotify')
    time.sleep(5)
    openApp('Spotify')
    time.sleep(5)
    cmd1 = 'osascript -e "tell application \\"Spotify\\"" -e "activate" -e "end tell"'
    cmd2 = 'osascript -e "tell application \\"Spotify\\"" -e "next track" -e "end tell"'
    Popen( cmd1, shell=True )
    time.sleep(5)
    Popen( cmd2, shell=True )


def openPage(URL):
	Popen(["open", "-a", "Google Chrome", URL])


def closeApp(APPNAME):
	cmd = 'osascript -e ' + "'" + 'quit app ' + '"' + str(APPNAME) + '"' + "'"
	Popen(cmd, shell=True)


def openApp(APPNAME):
	cmd = 'open -a ' + '"' + str(APPNAME) + '"'
	Popen(cmd, shell=True)

'''
I really don't like this option. it doens't do well to identify the coordinates of the user
'''
def ishome():
	api = PyiCloudService(EMAIL, ICLOUD)
	for i in api.devices:
		if IPHONE_ID in str(i):
			if i.location() is not None:
				place = i.location()
			else:
				place = dict()
				place['latitude'] = HOME_COORD['minlat']
				place['longitude'] = HOME_COORD['minlon']
	if HOME_COORD['minlat'] <= place['latitude'] <= HOME_COORD['maxlat']:
		if HOME_COORD['minlon'] <= place['longitude'] <= HOME_COORD['maxlon']:
			return True
		else:
			return False
	else:
		return False
