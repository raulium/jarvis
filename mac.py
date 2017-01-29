#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import BASE_PATH
# ============== EXTERNAL LIBRARIES
import time
from subprocess import Popen, os, PIPE


def setVolume(VALUE):
    '''
    ... for an ungodly reason, Apple has made it such that the volume scale
    is from 0 - 7. And real numbers. Meaning 3.5 is the center of the scale.
    ... w... t... f...
    '''
    Popen( ['osascript', '-e', 'set Volume' + str(VALUE)] )


def setLivingRoom():
    """ Set Audio Output to Living Room. """
    setVolume(7)
    Popen( ['osascript', BASE_PATH + 'AppleScripts/audioLivingRoom.applescript'] )
    time.sleep(1)


def setDisplay():
    """ Set Audio Output to Cinema Display. """
    setVolume(4)
    Popen( ['osascript', BASE_PATH + 'AppleScripts/audioDisplay.applescript'] )
    time.sleep(1)


# THIS DOESN'T APPEAR TO WORK... INVESTIGATE
# def lockScreen():
#     """Lock the screen"""
#     Popen(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'])


def notification(TITLE, MSG):
    """ Send notification to Notificaiton Center. """
    Popen(["osascript", "-e", "display notification " + '"' + MSG + '"' + " with title " + '"' + TITLE +'" sound name "Hero"'])


def ifMuted():
    out, err = Popen(['osascript', '-e', 'get volume settings'], stdout=PIPE ).communicate()
    l = out.split(',')
    if 'true' in str(l[3]):
        return 1
    else:
        return 0
