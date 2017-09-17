#!/usr/bin/python

# ============== EXTERNAL LIBRARIES
import time
import random
from datetime import datetime, timedelta
from atd import atd
# ============== CONFIG PARAMETERS\
from config import DOW, NAME, SNOOZE_TIME, NORMAL_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import GREETING, WAKE, say, laboratoryOptions, volunteerOptions, dayOffOptions, DAY_ASSES
from timing_mod import holidayDict, snooze, thirty_min_before, dto_to_string, getTime
from IFTTT_mod import IFTTT, IFTTTcmd
from lab_mod import labStatus
from mac_mod import setVolume, setDisplay, startMusic, openPage, ishome
from weather_mod import getSunsetDTO, newDailyReport
from math_mod import maths


# =======================================================================

# [Good] Morning [Raul]. | The time is [Time], and [All is well]. | [It seems today will be a] [beautiful] [day of the week]
# The temperature is [temp], with an expected high of [high] and a low of [low].
# [Bad conditions]
#    - conditions
#    - dew point
#    - dew point distance
# [Holiday condition]
# And may I also wish you a happy [holiday]

# NEW MORNING

def dayMessage(day_evaluation, bad_conditions, weather_segment, weekday):
    print("Bad Conditions: " + ', '.join(bad_conditions))
    day_segment = random.choice(DAY_ASSES) + day_evaluation + " " + DOW[weekday] + "."
    bad_segment = " "
    if len(bad_conditions) > 0:
        bad_segment = "Weather conditions to consider are: " + ', '.join(bad_conditions)
    holiday_segment = ""
    holString = holidayDict()
    if holString:
        holiday_segment = "And may I also wish you a happy " + holString + "."
    message = day_segment + ". " + weather_segment + ". " + bad_segment + ". " + holiday_segment + "."
    return message


def morningRoutine():
    WD = datetime.today().weekday()
    day_evaluation, bad_conditions, weather_segment = newDailyReport()
    statusMessage = dayMessage(day_evaluation, bad_conditions, weather_segment, WD)
    if WD >= 5:  # It's a weekend
        snooze(thirty_min_before(SNOOZE_TIME))
        IFTTT("sunrise")
        snooze(SNOOZE_TIME)
    else:
        if labStatus():  # Where "True" or "1" means closed
            if not holString:
                openPage("http://www.ll.mit.edu/status/index.html")
                statusMessage = "The laboratory appears to be closed today.  I've opened the lab's status page, if you care to learn more. " + statusMessage
            snooze(thirty_min_before(SNOOZE_TIME))
            IFTTT("sunrise")
            snooze(SNOOZE_TIME)
        else:
            snooze(thirty_min_before(NORMAL_TIME))
            IFTTT("sunrise")
            snooze(NORMAL_TIME)

    setVolume(5)
    setDisplay()

    sunset = getSunsetDTO()
    l = IFTTTcmd('living_room_lifx')
    w = IFTTTcmd('living_room_wink')
    atd.at(l, sunset)
    atd.at(w, sunset)

    startMusic()
    time.sleep(30)
    greeting_segment = random.choice(GREETING) + ", " + NAME + "."
    time_segment = "The time is " + getTime() + " " + random.choice(WAKE)
    say(greeting_segment + ". " + time_segment)

    time.sleep(40)

    myStatus = 0
    if datetime.today().weekday() <= 4:
        myStatus = laboratoryOptions()
    elif datetime.today().weekday() == 5:
        myStatus = volunteerOptions()
    else:
        myStatus = dayOffOptions()

    if myStatus < 1:
        maths()
        time.sleep(5)
        IFTTT("lights_on")
        IFTTT("wakeup")
        say(statusMessage)
    else:
        say("Everything has been taken care of. Feel free to go back to bed.")
