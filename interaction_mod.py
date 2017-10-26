#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
import random
import time
from subprocess import Popen
import speech_recognition as sr
from gmail_mod import sendGmail
# ============== CONFIG PARAMETERS
from config import NAME, WORK_LIST_STRING, ILL_MSG, WFH_MSG, VOLUNTEER_EMAIL, VOLUNTEER_ILL_MSG, VOLUNTEER_WFH_MSG
# ============== INTERNAL LIBRARIES
from mac_mod import check_process

# ============== CUSTOM REACTIONS & INTERACTION SPEECH

GREETING = ["Good morning", "Top of the morning", "Rise and shine",
            "Another dawn, another day", "Time to get up"]

WAKE = ["This is your monring wake up call.", "It is time to start your day.",
        "which means it's that time again.", "So let's not be lazy.",
        "And all is well."]

LAZY = ["It is time to get up.", "You can't blame anyone but yourself.",
        "It will only get worse from here if you don't get up."]

POSITIVE = ["Excellent!", "Perfect!", "Splended!", "Good enough.",
            "Wonderful.", "Outstanding!", "Marvelous!", "Great!", "Fantastic!",
            "Okay."]

NEGATIVE = ["Incorrect", "No.", "That's offensive",
            "Inferior performance", "R you even trying", "I think not.",
            "This is sad."]

WARN = [NAME + ", it's that time again.", "It is time to get ready for bed.",
        "The bells are tolling, " + NAME + ".", "Early to bed, early to rise."]

ILL_KEYS = ["not feeling well", "sick", "don't feel", "ill"]
WFH_KEYS = ["staying", "sleeping", "not going in", "day off", "working from home"]

DAY_ASSES = ["It seems today will be a", "It appears today will be a", "Today will be a",
             "It looks as though today might be a"]
GREAT = ["n amazing", " great", " beautiful", " terrific", " perfect"]
GOOD = [" good", " pretty good", " plesant", " favorable"]
OKAY = ["n alright", " decent", "n okay", " satisfactory"]
BAD = [" terrible", "bad", "unfavorable", "n unsatisfactory", "n ugly"]


# ============== INTERACTION functions


def say(STRING):
    cmd = 'say -v Lee "' + STRING + '"'
    Popen(cmd, shell=True)
    saytrap()


def saytrap():
    while (check_process('say') == True):
        continue


def laboratoryOptions():
    while 1:
        say("Are you ready to start your day?")
        reply = getReply()
        if reply is "ERR":
            say("I'm sorry, I didn't quite catch that.")
        elif reply is "NULL":
            mystring = NAME + " " + random.choice(LAZY)
            say(mystring)
        elif any(o in reply for o in ILL_KEYS):
            say("I'm sorry to hear that. Would you like me to contact the Laboratory?")
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                sendGmail(WORK_LIST_STRING, "Sick Day", ILL_MSG)
                return 1
            if 'no' in confirm:
                say("Then you shouldn't say you're feeling ill.")
                return 0
        elif any(o in reply for o in WFH_KEYS):
            say("Would you like me to notify the Laboratory?")
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                sendGmail(WORK_LIST_STRING, "WFH Today", WFH_MSG)
                return 0
            if 'no' in confirm:
                say("Then you should have said you were ready to start your day.")
                return 0
        else:
            say(random.choice(POSITIVE))
            break


def volunteerOptions():
    while 1:
        say("Are you ready to start your day?")
        reply = getReply()
        if reply is "ERR":
            say("I'm sorry, I didn't quite catch that.")
        elif reply is "NULL":
            mystring = NAME + " " + random.choice(LAZY)
            say(mystring)
        elif any(o in reply for o in ILL_KEYS):
            say("I'm sorry to hear that. Would you like me to contact the Museum?")
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                sendGmail(VOLUNTEER_EMAIL, "Out Sick", VOLUNTEER_ILL_MSG)
                return 1
            if 'no' in confirm:
                say("Then you shouldn't say you're feeling ill.")
                return 0
        elif any(o in reply for o in WFH_KEYS):
            say("Would you like me to notify the Museum?")
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                sendGmail(VOLUNTEER_EMAIL, "Out Today", VOLUNTEER_WFH_MSG)
                return 1
            if 'no' in confirm:
                say("Then you should have said you were ready to start your day.")
                return 0
        else:
            say(random.choice(POSITIVE))
            break


def dayOffOptions():
    while 1:
        say("Are you ready to start your day?")
        reply = getReply()
        if reply is "ERR":
            say("I'm sorry, I didn't quite catch that.")
        elif reply is "NULL":
            mystring = NAME + " " + random.choice(LAZY)
            say(mystring)
        else:
            say(random.choice(POSITIVE))
            break


def getReply():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10)
        try:
            reply = r.recognize_google(audio)
        except LookupError:
            reply = "ERR"  # Bad input condition
    except sr.WaitTimeoutError:
        reply = "NULL"  # Nil heard
    except sr.UnknownValueError:
        reply = "ERR"  # Bad input condition
    return reply  # Return transcript of reply


def micTest():
    say("Voice authorization required.")
    r = getReply()
    if 'authorization' in r:
        r = r.split('authorization')
        r = r[1]
    time.sleep(0.2)
    say(r + " recieved.")
    say('Authorization accepted.  Hello, ' + NAME + ".")