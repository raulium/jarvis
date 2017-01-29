#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import IFFT_KEY
# ============== EXTERNAL LIBRARIES
import urllib
from BeautifulSoup import BeautifulSoup as bsp


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'


def ripText(URL):
    soup = bsp(urllib.urlopen(URL).read())
    p = soup.body.div.findAll('p')
    strings = str(p[0])
    strings = re.sub("<p>", '', strings)
    strings = re.sub("</p>", '', strings)
    strings = strings.split('.')
    return strings


def labStatus():
    """ Check status of the Laboratory, returning 0 if open and 1 if closed. """
    status = None
    statMSG = ripText('http://www.ll.mit.edu/status/index.hmtl')
    if "closed" in str(statMSG[0]):
        status = 1
    if "open" in str(statMSG[0]):
        status = 0
    return status


def IFFT(EVENT):
    url = 'https://maker.ifttt.com/trigger/' + EVENT + '/with/key/' + IFFT_KEY
    Popen( ['curl', '-X', 'POST', url] )


# STOPPED WORKING -- FIX THIS
# def startRadio():
#     openPage("http://www.wgbh.org/audioPlayers/wgbh.cfm")


def startMusic():
    cmd = 'osascript -e "tell application \\"Spotify\\"" -e "activate" -e "delay 5" -e "next track" -e "end tell"'
    Popen( cmd, shell=True )


def openPage(URL):
    Popen( ['open', URL] )
