#!/usr/local/env python

# ============== CONFIG PARAMETERS
# ============== INTERNAL LIBRARIES
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
