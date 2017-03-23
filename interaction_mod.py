#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import NAME
# ============== INTERNAL LIBRARIES
from mac_mod import setVolume
# ============== EXTERNAL LIBRARIES
import time, random
import speech_recognition as sr
from subprocess import Popen, os, PIPE


# ============== CUSTOM REACTIONS & INTERACTION SPEECH

GREETING = ["Good morning", "Top of the morning", "Rise and shine",
            "Another dawn, another day"]

WAKE = ["This is your monring wake up call.", "It is time to start your day.",
        "which means it's that time again.", "So let's not be lazy."]

UNFINISHED = ["Because you haven't finished my programming",
                "Due to the fact I am an unfinnished project",
                "As I have been given no external sensors"]

LAZY = ["It is time to get up.", "You can't blame anyone but yourself.",
            "It will only get worse from here if you don't get up."]

POSITIVE = ["Excellent!", "Perfect!", "Splended!", "Good enough.",
            "Wonderful.", "Outstanding!", "Marvelous!", "Great!", "Fantastic!",
            "Okay."]

NEGATIVE = ["Incorrect", "No.", "That's weak", "That's offensive",
            "Inferior performance", "R you even trying", "I think not.",
            "This is sad."]

WARN = [NAME + ", it's that time again.", "It is time to get ready for bed.",
        "The bells are tolling, " + NAME + ".", "Early to bed, early to rise."]

ILL_KEYS=["not feeling well", "sick", "don't feel", "ill"]
WFH_KEYS=["staying", "sleeping", "not going in", "day off"]

# ============== INTERACTION functions


def say(STRING):
    Popen( ['say', '-v', 'Lee', STRING] )


def saiff(STRING, FILENAME):    # I really don't know why I made this. Speech system todo?
    Popen( ['say', '-v' 'Lee', '-o', str(FILENAME), str(STRING)] )


def morningUserCheck():
    while(1):
        say("Are you ready to start your day?")
        reply = getReply()
        if reply is "ERR":
            say("I'm sorry, I didn't quite catch that.")
            time.sleep(2.5) # this might be where the saiff function would work
        elif reply is "NULL":
            mystring = NAME + " " + random.choice(LAZY)
            say(mystring)
            time.sleep(3)
        elif any(o in reply for o in ILL_KEYS):
            say("I'm sorry to hear that. Would you like me to contact the Laboratory?")
            time.sleep(2.5)
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                # SEND SICK MESSAGE HERE
                time.sleep(2.5)
                break
            if 'no' in confirm:
                say("Then you shouldn't say you're feeling ill.")
                time.sleep(2.5)
                continue
        elif any(o in reply for o in WFH_KEYS):
            say("Would you like me to notify the Laboratory?")
            time.sleep(2.5)
            confirm = getReply()
            if 'yes' in confirm:
                say("Very well. Sending message now.")
                # SEND WFM MESSAGE HERE
                time.sleep(2)
                break
            if 'no' in confirm:
                say("Then you should have said you were ready to start your day.")
                time.sleep(3.5)
                break
        else:
            say(random.choice(POSITIVE))
            time.sleep(2)
            break

def getReply():
    time.sleep(2)
    setVolume(1)
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout = 10)
        try:
            reply = r.recognize_google(audio)
        except LookupError:
            reply = "ERR"       # Bad input condition
    except sr.WaitTimeoutError:
        reply = "NULL"          # Nil heard
    except sr.UnknownValueError:
        reply = "ERR"           # Bad input condition
    setVolume(4)
    time.sleep(0.5)
    return reply                # Return transcript of reply

# ============== TEXTING FUNCTIONS -- REQUIRES REFACTORING AND TESTING
# def jarvisTEXT(PERSON, MESSAGE):
#     client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         to=CONTACTS[PERSON],
#         from_="+15097613225",
#         body=MESSAGE
#     )

# def text(PERSON, MESSAGE):
#     conString = 'tell application "Messages" to send "' + MESSAGE + '" to buddy "' + PERSON + '" of service "SMS"'
#     Popen(['osascript', '-e', conString])
