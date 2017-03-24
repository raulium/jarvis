#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import NAME, SNOOZE_TIME, READING_TIME, BED_TIME, NORMAL_TIME, DOW, MASTERKEY, HOST_IP
# ============== INTERNAL LIBRARIES
from vacation_mod import away, back, vMorningRoutine, vEveningRoutine
from interaction_mod import say
from mac_mod import startMusic
from morning_mod import morningRoutine
from evening_mod import eveningRoutine
from weather_mod import dailyReport
from IFTTT_mod import IFTTT
# ============== EXTERNAL LIBRARIES
import logging
from flask import Flask, jsonify, request, current_app, abort
from subprocess import Popen
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
	abort(404)

@app.route('/away', methods=['POST'])
def iaway():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			away()
			return str(datetime.now()) + ":\tTEST - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/back', methods=['POST'])
def iback():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			back()
			return str(datetime.now()) + ":\tTEST - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/test', methods=['POST'])
def testing():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			say("Test complete. All systems are functioning as expected.")
			return str(datetime.now()) + ":\tTEST - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/morning', methods=['POST'])
def morn_func():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			if VACATION:
				vMorningRoutine()
			else:
				morningRoutine()
			return str(datetime.now()) + ":\tMORNING - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/evening', methods=['POST'])
def eve_func():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			if VACATION:
				vEveningRoutine()
			else:
				eveningRoutine()
			return str(datetime.now()) + ":\tEVENING - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/current', methods=['POST'])
def get_curr():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))
		print "JSON Recieved -- " + str(data)

		if MASTERKEY in data["key"]:
			dailyReport()
			Popen(["afplay", "/tmp/DailyReport.aiff"])
			return str(datetime.now()) + ":\tCURRENT - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/movie', methods=['POST'])
def movie_time():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			IFTTT('dim_lighting')
			IFTTT('movie_time')
			return str(datetime.now()) + ":\tMOVIE TIME - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

@app.route('/music', methods=['POST'])
def music_time():
	data = request.get_json(force=True)

	if data is not None:
		app.logger.debug("JSON Recieved -- " + str(data))

		if MASTERKEY in data["key"]:
			startMusic()
			return str(datetime.now()) + ":\tMUSIC TIME - SUCCESS!\n"
		else:
			abort(404)
	else:
		app.logger.debug("No JSON recieved")
		abort(404)

if __name__=='__main__':
	# logger = logging.getLogger('werkzeug')
	# handler = logging.FileHandler('access.log')
	# app.logger.setLevel(logging.INFO) # use the native logger of flask
	# app.logger.addHandler(handler)
	app.run(host=HOST_IP, threaded=True, debug=True)
