#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import READING_TIME, BED_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import WARN, saiff
from timing_mod import getCurrentTime, snooze, t_minus
from mac_mod import notification, setLivingRoom, setDisplay
from IFTTT_mod import IFTTT
# ============== EXTERNAL LIBRARIES
import time
import random


def eveningRoutine():

    h, m, t = getCurrentTime()
    timestring = str(h) + ":" + str(m) + " " + t
    title = "Time Notification"
    msg = "It is " + timestring + "."
    notification(title, msg)

    snooze(t_minus(READING_TIME, 10))

    h, m, t = getCurrentTime()
    timestring = str(h) + ":" + str(m) + " " + t
    title = "Time Notification"
    msg = "It is " + timestring + "."
    notification(title, msg)
    notification(title, msg)

    rmsg = random.choice(WARN) + " It is " + timestring + "."

    setLivingRoom()
    time.sleep(1)
    saiff(rmsg, 'evening')
    setDisplay()

    notification(title, "This computer will lock in 10 min.")
    snooze(READING_TIME)

    IFTTT("reading")

    snooze(t_minus(BED_TIME, 5))
    IFTTT("light_notice")
    snooze(BED_TIME)
    IFTTT("light_notice")
    IFTTT("sunset")
    IFTTT("lights_off")
