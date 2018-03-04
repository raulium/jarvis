#!/usr/bin/python

# ============== CONFIG PARAMETERS
from config import MASTERKEY, HOST_IP, BASE_PATH
# ============== INTERNAL LIBRARIES
from vacation_mod import vMorningRoutine, vEveningRoutine, checkVacationStatus, setVacation, rmVacation
from interaction_mod import say, micTest
from mac_mod import startMusic, setLivingRoom, setDisplay
from morning_mod import morningRoutine, dayMessage
from evening_mod import eveningRoutine
from IFTTT_mod import IFTTT
# ============== EXTERNAL LIBRARIES
import time
import sys
import logging
from flask import Flask, request, abort
from subprocess import Popen
from datetime import datetime

app = Flask(__name__)


def data_check():
    data = request.get_json(force=True)

    if data is not None:
        app.logger.debug("JSON Recieved -- " + str(data))

        if MASTERKEY in data["key"]:
            return True
        else:
            app.logger.debug("Bad Key")
            return False
    else:
        app.logger.debug("No JSON recieved")
        return False


def apiReturn(myString):
    return str(datetime.now()) + ":\t" + myString + "\t -- SUCCESS!\n"


@app.route('/')
def index():
    abort(404)


# @app.route('/away', methods=['POST'])
# def iaway():
# 	data = request.get_json(force=True)
#
# 	if data is not None:
# 		app.logger.debug("JSON Recieved -- " + str(data))
#
# 		if MASTERKEY in data["key"]:
# 			away()
# 			return str(datetime.now()) + ":\tTEST - SUCCESS!\n"
# 		else:
# 			abort(404)
# 	else:
# 		app.logger.debug("No JSON recieved")
# 		abort(404)
#
# @app.route('/back', methods=['POST'])
# def iback():
# 	data = request.get_json(force=True)
#
# 	if data is not None:
# 		app.logger.debug("JSON Recieved -- " + str(data))
#
# 		if MASTERKEY in data["key"]:
# 			back()
# 			return str(datetime.now()) + ":\tTEST - SUCCESS!\n"
# 		else:
# 			abort(404)
# 	else:
# 		app.logger.debug("No JSON recieved")
# 		abort(404)

@app.route('/load', methods=['POST'])
def loading():
    f = "LOADING"
    status = data_check()
    if status:
        say("Loading system services.")
        return apiReturn(f)
    else:
        abort(404)


@app.route('/away', methods=['POST'])
def gone():
    f = 'AWAY'
    status = data_check()
    if status:
        if checkVacationStatus():
            say('Vacation mode already active.')
            return apiReturn('REDUNDANT')
        setVacation()
        say("Vacation mode activated.")
        return apiReturn(f)
    else:
        abort(404)


@app.route('/back', methods=['POST'])
def here():
    f = 'BACK'
    status = data_check()
    if status:
        if not checkVacationStatus():
            say("Vacation mode already deactivated.")
            return apiReturn("REDUNDANT")
        rmVacation()
        say("Vacation mode deactivated.")
        return apiReturn(f)
    else:
        abort(404)


@app.route('/test', methods=['POST'])
def testing():
    f = "TESTING"
    status = data_check()
    if status:
        say("Test complete. All systems are functioning as expected.")
        return apiReturn(f)
    else:
        abort(404)


@app.route('/morning', methods=['POST'])
def morn_func():
    f = "MORNING"
    status = data_check()
    if status:
        if checkVacationStatus():
            vMorningRoutine()
        else:
            morningRoutine()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/evening', methods=['POST'])
def eve_func():
    f = "EVENING"
    status = data_check()
    if status:
        if checkVacationStatus():
            vEveningRoutine()
        else:
            eveningRoutine()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/movie', methods=['POST'])
def movie_time():
    f = "MOVIE"
    status = data_check()
    if status:
        IFTTT('dim_lighting')
        IFTTT('movie_time')
        return apiReturn(f)
    else:
        abort(404)


@app.route('/music', methods=['POST'])
def music_time():
    f = "MUSIC"
    status = data_check()
    if status:
        startMusic()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/living', methods=['POST'])
def living():
    f = "LIVINGROOM"
    status = data_check()
    if status:
        setLivingRoom()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/display', methods=['POST'])
def display():
    f = "DISPLAY"
    status = data_check()
    if status:
        setDisplay()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/mic', methods=['POST'])
def mic():
    f = "MIC"
    status = data_check()
    if status:
        micTest()
        return apiReturn(f)
    else:
        abort(404)


@app.route('/redalert', methods=['POST'])
def redalert():
    f = "REDALERT"
    status = data_check()
    if status:
        setLivingRoom()
        time.sleep(3)
        IFTTT('dim_lighting')
        Popen(["afplay", BASE_PATH + "/git/jarvis/redalert.mp3"])
        IFTTT('klaxon')
        time.sleep(10)
        setDisplay()
        return apiReturn(f)
    else:
        abort(404)

@app.route('/weather', methods=['POST'])
def current():
    f = "WEATHER"
    status = data_check()
    if status:
        msg = dayMessage()
        say(msg)
        return apiReturn(f)
    else:
        abort(404)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app.run(host=HOST_IP, threaded=True, debug=True)
