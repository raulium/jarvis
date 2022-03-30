#!/usr/bin/python

# ============== EXTERNAL LIBRARIES
import time
import random
from datetime import datetime
from atd import atd
# ============== CONFIG PARAMETERS\
from config import DOW, NAME, SNOOZE_TIME, NORMAL_TIME
# ============== INTERNAL LIBRARIES
from interaction_mod import GREETING, WAKE, say, laboratoryOptions, volunteerOptions, dayOffOptions, DAY_ASSES
from timing_mod import holidayDict, snooze, t_minus, getTime
from IFTTT_mod import IFTTT, IFTTTcmd
from lab_mod import labStatus
from mac_mod import setVolume, setDisplay, startMusic, openPage
from weather_mod import getSunsetDTO, newDailyReport
from math_mod import maths
from motivation_mod import daysToWeekend, weeksToDate, counterString, motivate


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

def dayMessage():
    WD = datetime.today().weekday()
    day_evaluation, bad_conditions, weather_segment = newDailyReport()
    print("Bad Conditions: " + ', '.join(bad_conditions))
    day_segment = random.choice(DAY_ASSES) + day_evaluation + " " + DOW[WD] + "."
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
    statusMessage = dayMessage()
    if WD >= 5:  # It's a weekend
        snooze(t_minus(SNOOZE_TIME, 30))
        IFTTT("sunrise")
        snooze(SNOOZE_TIME)
    else:
        if labStatus():  # Where "True" or "1" means closed
            if not holString:
                openPage("http://www.ll.mit.edu/status/index.html")
                statusMessage = "The laboratory appears to be closed today.  I've opened the lab's status page, if you care to learn more. " + statusMessage
            snooze(t_minus(SNOOZE_TIME, 30))
            IFTTT("sunrise")
            snooze(SNOOZE_TIME)
        else:
            snooze(t_minus(NORMAL_TIME, 30))
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
        semesterEnd = datetime(2018, 06, 22)
        say(counterString(daysToWeekend(), "day") + " the weekend, and " + counterString(weeksToDate(semesterEnd),"week") + " the Chad returns.")
        say(motivate())

    else:
        say("Everything has been taken care of. Feel free to go back to bed.")
