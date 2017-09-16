#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
import time
import random
# ============== CONFIG PARAMETERS
# ============== INTERNAL LIBRARIES
from interaction_mod import POSITIVE, NEGATIVE, say, getReply


def do_math():  # COULD USE REWORK. WHAT HAPPENS IF YOU NEVER HEAR A REPLY? (BREAK!)
    """
    Function poses the user a math problem, evaluates the response
    and determines if the user got the problem right (1) or wrong (0)
    """
    val1 = random.randint(3, 9)
    val2 = random.randint(6, 9)
    answer = val1 * val2

    say('What is ' + str(val1) + ' multiplied by ' + str(val2) + '?')
    reply = getReply()
    answer_status = 0
    try:
        reply = int(reply)
    except ValueError:
        say(random.choice(NEGATIVE))
        answer_status = 0
    if reply == answer:
        say(random.choice(POSITIVE))
        answer_status = 1
    else:
        say(random.choice(NEGATIVE))
        answer_status = 0
    return answer_status


def maths():  # Maybe rename this?
    """
    Function traps user in a loop, requiring the user to answer three (3)
    math problems correctly before exiting.
    """
    say("How about a little exercise?")
    i = 0
    while i < 3:
        result = do_math()
        if result < 1:
            i = 0
        else:
            i += result


def main():
    """ run maths """
    maths()


if __name__ == '__main__':
    main()
