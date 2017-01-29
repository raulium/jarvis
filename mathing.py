#!/usr/local/env python

# ============== INTERNAL LIBRARIES
from interactionlib import POSITIVE, NEGATIVE, say, getReply
# ============== EXTERNAL LIBRARIES
import time, random
import speech_recognition as sr
from subprocess import Popen, os, PIPE


def doMath():   # COULD USE REWORK. WHAT HAPPENS IF YOU NEVER HEAR A REPLY? (BREAK!)
    val1 = random.randint(3,9)
    val2 = random.randint(6,9)
    answer = val1 * val2

    say('What is ' + str(val1) + ' multiplied by ' + str(val2) + '?')
    time.sleep(1)   # THIS IS HIGHLY PROBLEMATIC TO BE RELYING UPON ALL THE TIME
    reply = getReply()
    print "Answer:\t" + str(answer)
    print "Reply:\t" + str(reply)
    try:
        reply = int(reply)
    except ValueError:
        say(random.choice(NEGATIVE))
        time.sleep(2)
        return 0

    if (reply == answer):
        say(random.choice(POSITIVE))
        time.sleeo(2)
        return 1
    else:
        say(random.choice(NEGATIVE))
        time.sleep(2)
        return 0


def fuckGreg(): # Maybe rename this?
    say("How about a little exercise?")
    time.sleep(3)
    i = 0
    while i < 3:
        result = doMath()
        if result < 1:
            i = 0
        else:
            i += result


def main():
    fuckGreg()


if __name__=='__main__':
    main()
