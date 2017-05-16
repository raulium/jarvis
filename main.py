#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import NAME, SNOOZE_TIME, READING_TIME, BED_TIME, NORMAL_TIME, DOW, MASTERKEY, HOST_IP
# ============== INTERNAL LIBRARIES
from vacation_mod import away, back, vMorningRoutine, vEveningRoutine
from interaction_mod import say
from mac_mod import startMusic, setVolume
from morning_mod import morningRoutine
from evening_mod import eveningRoutine
from weather_mod import dailyReport
from IFTTT_mod import IFTTT
# ============== EXTERNAL LIBRARIES
import logging, json
from flask import Flask, jsonify, request, current_app, abort
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

VACATION = False

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
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/test', methods=['POST'])
def testing():
	f = "TESTING"
	status = data_check()
	if status:
		say("Test complete. All systems are functioning as expected.")
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/morning', methods=['POST'])
def morn_func():
	f = "MORNING"
	status = data_check()
	if status:
		if VACATION:
			vMorningRoutine()
		else:
			morningRoutine()
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/evening', methods=['POST'])
def eve_func():
	f = "EVENING"
	status = data_check()
	if status:
		if VACATION:
			vEveningRoutine()
		else:
			eveningRoutine()
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/current', methods=['POST'])
def get_curr():
	f = "WEATHER"
	status = data_check()
	if status:
		dailyReport()
		Popen(["afplay", "/tmp/DailyReport.aiff"])
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/movie', methods=['POST'])
def movie_time():
	f = "MOVIE"
	status = data_check()
	if status:
		IFTTT('dim_lighting')
		IFTTT('movie_time')
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/music', methods=['POST'])
def music_time():
	f = "MUSIC"
	status = data_check()
	if status:
		startMusic()
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

@app.route('/vol', methods=['POST'])
def volume():
	f = "VOLUME"
	status = data_check()
	if status:
		setVolume(7)
		return str(datetime.now()) + ":\t" + f + "\t -- SUCCESS!\n"
	else:
		abort(404)

if __name__=='__main__':
	# logger = logging.getLogger('werkzeug')
	# handler = logging.FileHandler('access.log')
	# app.logger.setLevel(logging.INFO) # use the native logger of flask
	# app.logger.addHandler(handler)
	app.run(host=HOST_IP, threaded=True, debug=True)
