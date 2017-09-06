#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
import random
import time

# ============== CONFIG PARAMETERS
from config import NAME

# ============== INTERNAL LIBRARIES
from interaction_mod import POSITIVE, say
from mac_mod import setVolume


def stretch_Spinal():
    say('Sit cross-legged.')
    time.sleep(5)
    i = 0
    while i < 2:
        say('Twist left.')
        time.sleep(10)
        say('Return to center.')
        time.sleep(5)
        say('Twist right.')
        time.sleep(10)
        say('Return to center.')
        time.sleep(5)
        i += 1
    say('Put your left hand on the floor. Inhale. Raise your right arm. While exhaling, reach left.')
    time.sleep(10)
    say('Inhale, and relax a moment.')
    time.sleep(5)
    say('Exhale and reach left, again.')
    time.sleep(10)
    say('Time to switch.')
    time.sleep(5)
    say('Put your right hand on the floor. Inhale. Raise your left arm. While exhaling, reach right.')
    time.sleep(10)
    say('Inhale, and relax a moment.')
    time.sleep(5)
    say('Exhale and reach right, again.')
    time.sleep(10)


def stretch_Cat():
    say('Come to all fours')
    time.sleep(5)
    i = 0
    while i < 3:
        say('Curve your back toward the ceiling. Drawing your chin to your stomach.')
        time.sleep(10)
        say('Inhale deeply')
        time.sleep(5)
        say('Exhale and arch your back.')
        time.sleep(5)
        say('Slowly raise your head to the ceiling.')
        time.sleep(5)
        i += 1


def stretch_Lunge():
    say('Come to all fours')
    time.sleep(5)
    i = 0
    while i < 3:
        say('Lunge with your right foot')
        time.sleep(5)
        say("Don't forget to breathe.")
        time.sleep(5)
        say('Lunge with left foot.')
        time.sleep(10)
        i += 1


def fuckGreg2():
    setVolume(3)
    say("I've been instructed to try to further motivate you, " + NAME + ".")
    time.sleep(5)
    say('Now for a real exercise. Stretching.')
    time.sleep(5)
    stretch_Spinal()
    stretch_Cat()
    stretch_Lunge()
    say(random.choice(POSITIVE) + 'All done. I hope that woke you up.')
