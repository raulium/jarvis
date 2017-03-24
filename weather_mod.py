#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import WUNDERGROUND_KEY
# ============== INTERNAL LIBRARIES
from web_mod import MyOpener
from interaction_mod import saiff
# ============== EXTERNAL LIBRARIES
import json, email
from datetime import datetime


def dailyReport():
	data = getWeatherJSON('current')

	conditions = data['current_observation']['weather']

	feels_like = data['current_observation']['feelslike_f']
	temp = data['current_observation']['temp_f']

	observation_time = datetime.fromtimestamp(email.Utils.mktime_tz(email.Utils.parsedate_tz(data['current_observation']['observation_time_rfc822'])))
	observation_time = observation_time.strftime("%I:%M %p")

	data = getWeatherJSON('forecast')

	high = data['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
	low = data['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']

	if temp >= feels_like:
		temperature_string = "The temperature is " + str(temp) + " degrees, with a high of " + str(high) + " and a low of " + str(low) + "."
	else:
		temperature_string = "Though the temperature is " + str(temp) + ", it feels like " + str(feels_like) + " degrees.  It's expected to reach " + str(high) + " today, with a low of " + str(low) + "."

	fullReport = "As of " + str(observation_time) + " it is currently " + conditions + "." + temperature_string
	saiff(fullReport, "/tmp/DailyReport.aiff")

def getWeatherJSON(weather_type):
	if weather_type == 'current':
		url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/conditions/q/MA/waltham.json"
	if weather_type == 'forecast':
		url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/forecast/q/MA/waltham.json"
	agent = MyOpener()
	page = agent.open(url)
	jsonurl = page.read()
	data = json.loads(jsonurl)
	return data
