#!/usr/local/env python

# ============== EXTERNAL LIBRARIES
import email
import json
import math
import random
from datetime import datetime, timedelta
from web_mod import MyOpener
# ============== CONFIG PARAMETERS
from config import WUNDERGROUND_KEY
# ============== INTERNAL LIBRARIES
from interaction_mod import GREAT, GOOD, OKAY, BAD
from timing_mod import whatSeason

WEATHER_SCORE = {
    # SPRING, SUMMER, FALL, WINTER
    'HeavyBlowing Sand': [0.2, 0.2, 0.2, 0.2],
    'Blowing Sand': [0.3, 0.3, 0.3, 0.3],
    'LightBlowing Sand': [0.3, 0.3, 0.3, 0.3],
    'HeavyBlowing Snow': [0.1, 0.0, 0.1, 0.4],
    'Blowing Snow': [0.2, 0.0, 0.2, 0.5],
    'LightBlowing Snow': [0.3, 0.0, 0.3, 0.6],
    'HeavyBlowing Widespread Dust': [0.2, 0.2, 0.2, 0.2],
    'Blowing Widespread Dust': [0.3, 0.3, 0.3, 0.3],
    'LightBlowing Widespread Dust': [0.4, 0.4, 0.4, 0.4],
    'Clear': [1, 1, 1, 1],
    'HeavyDrizzle': [0.7, 0.8, 0.6, 0.5],
    'Drizzle': [0.8, 0.9, 0.7, 0.6],
    'LightDrizzle': [0.9, 0.9, 0.8, 0.7],
    'HeavyDust Whirls': [0.1, 0.1, 0.1, 0.1],
    'Dust Whirls': [0.2, 0.2, 0.2, 0.2],
    'LightDust Whirls': [0.3, 0.3, 0.3, 0.3],
    'HeavyFog': [0.8, 0.9, 0.7, 0.7],
    'Fog': [0.9, 0.9, 0.8, 0.8],
    'LightFog': [1, 1, 0.9, 0.9],
    'HeavyFog Patches': [0.9, 0.9, 0.8, 0.8],
    'Fog Patches': [1, 1, 0.9, 0.9],
    'LightFog Patches': [1, 1, 0.9, 0.9],
    'HeavyFreezing Drizzle': [0.1, 0.0, 0.1, 0.4],
    'Freezing Drizzle': [0.2, 0.0, 0.2, 0.5],
    'LightFreezing Drizzle': [0.3, 0.0, 0.3, 0.6],
    'HeavyFreezing Fog': [0.1, 0.0, 0.1, 0.4],
    'Freezing Fog': [0.2, 0.0, 0.2, 0.5],
    'LightFreezing Fog': [0.3, 0.0, 0.3, 0.6],
    'HeavyFreezing Rain': [0.1, 0.0, 0.1, 0.4],
    'Freezing Rain': [0.2, 0.0, 0.2, 0.5],
    'LightFreezing Rain': [0.3, 0.0, 0.3, 0.6],
    'Funnel Cloud': [0.0, 0.0, 0.0, 0.0],
    'HeavyHail': [0.3, 0.4, 0.3, 0.4],
    'Hail': [0.4, 0.5, 0.4, 0.5],
    'LightHail': [0.5, 0.6, 0.5, 0.6],
    'HeavyHail Showers': [0.2, 0.3, 0.2, 0.3],
    'Hail Showers': [0.3, 0.4, 0.3, 0.4],
    'LightHail Showers': [0.4, 0.5, 0.4, 0.5],
    'HeavyHaze': [0.3, 0.3, 0.3, 0.3],
    'Haze': [0.4, 0.4, 0.4, 0.4],
    'LightHaze': [0.5, 0.5, 0.5, 0.5],
    'HeavyIce Crystals': [0.1, 0.0, 0.1, 0.4],
    'Ice Crystals': [0.2, 0.0, 0.2, 0.5],
    'LightIce Crystals': [0.3, 0.0, 0.3, 0.6],
    'HeavyIce Pellet Showers': [0.1, 0.0, 0.1, 0.4],
    'Ice Pellet Showers': [0.2, 0.0, 0.2, 0.5],
    'LightIce Pellet Showers': [0.3, 0.0, 0.3, 0.6],
    'HeavyIce Pellets': [0.1, 0.0, 0.1, 0.4],
    'Ice Pellets': [0.2, 0.0, 0.2, 0.5],
    'LightIce Pellets': [0.3, 0.0, 0.3, 0.6],
    'HeavyLow Drifting Sand': [0.5, 0.5, 0.5, 0.5],
    'Low Drifting Sand': [0.6, 0.6, 0.6, 0.6],
    'LightLow Drifting Sand': [0.7, 0.7, 0.7, 0.7],
    'HeavyLow Drifting Snow': [0.1, 0.0, 0.1, 0.4],
    'Low Drifting Snow': [0.2, 0.0, 0.2, 0.5],
    'LightLow Drifting Snow': [0.3, 0.0, 0.3, 0.6],
    'HeavyLow Drifting Widespread Dust': [0.3, 0.3, 0.3, 0.3],
    'Low Drifting Widespread Dust': [0.4, 0.4, 0.4, 0.4],
    'LightLow Drifting Widespread Dust': [0.5, 0.5, 0.5, 0.5],
    'HeavyMist': [0.6, 0.7, 0.5, 0.5],
    'Mist': [0.7, 0.8, 0.6, 0.6],
    'LightMist': [0.8, 0.9, 0.7, 0.7],
    'Mostly Cloudy': [0.9, 1, 0.9, 0.9],
    'Overcast': [0.8, 0.9, 0.7, 0.7],
    'Partial Fog': [0.7, 0.8, 0.7, 0.7],
    'Partly Cloudy': [1, 1, 0.9, 1],
    'Patches of Fog': [0.7, 0.8, 0.7, 0.7],
    'HeavyRain': [0.8, 0.9, 0.7, 0.6],
    'Rain': [0.9, 0.9, 0.8, 0.7],
    'LightRain': [0.9, 1, 0.9, 0.8],
    'HeavyRain Mist': [0.8, 0.9, 0.7, 0.6],
    'Rain Mist': [0.9, 0.9, 0.8, 0.7],
    'LightRain Mist': [1, 1, 0.9, 0.8],
    'HeavyRain Showers': [0.6, 0.7, 0.5, 0.5],
    'Rain Showers': [0.7, 0.8, 0.6, 0.6],
    'LightRain Showers': [0.8, 0.9, 0.7, 0.7],
    'HeavySand': [0.3, 0.3, 0.3, 0.3],
    'Sand': [0.4, 0.4, 0.4, 0.4],
    'LightSand': [0.5, 0.5, 0.5, 0.5],
    'HeavySandstorm': [0.2, 0.2, 0.2, 0.2],
    'Sandstorm': [0.3, 0.3, 0.3, 0.3],
    'LightSandstorm': [0.4, 0.4, 0.4, 0.4],
    'Scattered Clouds': [1, 1, 1, 1],
    'Shallow Fog': [0.7, 0.8, 0.7, 0.7],
    'Small Hail': [0.5, 0.6, 0.5, 0.6],
    'HeavySmall Hail Showers': [0.4, 0.5, 0.3, 0.5],
    'Small Hail Showers': [0.5, 0.6, 0.4, 0.6],
    'LightSmall Hail Showers': [0.6, 0.7, 0.5, 0.7],
    'HeavySmoke': [0.3, 0.3, 0.3, 0.3],
    'Smoke': [0.4, 0.4, 0.4, 0.4],
    'LightSmoke': [0.5, 0.5, 0.5, 0.5],
    'HeavySnow': [0.1, 0.0, 0.1, 0.4],
    'Snow': [0.2, 0.0, 0.2, 0.5],
    'LightSnow': [0.3, 0.0, 0.3, 0.6],
    'HeavySnow Blowing Snow Mist': [0.1, 0.0, 0.1, 0.4],
    'Snow Blowing Snow Mist': [0.2, 0.0, 0.2, 0.5],
    'LightSnow Blowing Snow Mist': [0.3, 0.0, 0.3, 0.6],
    'HeavySnow Grains': [0.2, 0.0, 0.2, 0.5],
    'Snow Grains': [0.3, 0.0, 0.3, 0.6],
    'LightSnow Grains': [0.4, 0.0, 0.4, 0.7],
    'HeavySnow Showers': [0.0, 0.0, 0.0, 0.5],
    'Snow Showers': [0.1, 0.0, 0.1, 0.6],
    'LightSnow Showers': [0.2, 0.0, 0.2, 0.7],
    'HeavySpray': [0.2, 0.2, 0.2, 0.2],
    'Spray': [0.3, 0.3, 0.3, 0.3],
    'LightSpray': [0.4, 0.4, 0.4, 0.4],
    'Squalls': [0.5, 0.5, 0.5, 0.5],
    'HeavyThunderstorm': [0.6, 0.7, 0.6, 0.5],
    'Thunderstorm': [0.7, 0.8, 0.7, 0.6],
    'LightThunderstorm': [0.8, 0.9, 0.8, 0.7],
    'HeavyThunderstorms and Ice Pellets': [0.4, 0.5, 0.4, 0.5],
    'Thunderstorms and Ice Pellets': [0.5, 0.6, 0.5, 0.6],
    'LightThunderstorms and Ice Pellets': [0.6, 0.7, 0.6, 0.7],
    'HeavyThunderstorms and Rain': [0.5, 0.6, 0.5, 0.4],
    'Thunderstorms and Rain': [0.6, 0.7, 0.6, 0.5],
    'LightThunderstorms and Rain': [0.7, 0.8, 0.7, 0.6],
    'HeavyThunderstorms and Snow': [0.0, 0.0, 0.0, 0.3],
    'Thunderstorms and Snow': [0.1, 0.0, 0.1, 0.4],
    'LightThunderstorms and Snow': [0.2, 0.0, 0.2, 0.5],
    'HeavyThunderstorms with Hail': [0.4, 0.5, 0.4, 0.5],
    'Thunderstorms with Hail': [0.5, 0.6, 0.5, 0.6],
    'LightThunderstorms with Hail': [0.6, 0.7, 0.6, 0.7],
    'HeavyThunderstorms with Small Hail': [0.5, 0.6, 0.5, 0.6],
    'Thunderstorms with Small Hail': [0.6, 0.7, 0.6, 0.7],
    'LightThunderstorms with Small Hail': [0.7, 0.8, 0.7, 0.8],
    'Unknown': [0.5, 0.5, 0.5, 0.5],
    'Unknown Precipitation': [0.9, 0.9, 0.7, 0.6],
    'HeavyVolcanic Ash': [0.0, 0.0, 0.0, 0.0],
    'Volcanic Ash': [0.0, 0.0, 0.0, 0.0],
    'LightVolcanic Ash': [0.0, 0.0, 0.0, 0.0],
    'HeavyWidespread Dust': [0.2, 0.2, 0.2, 0.2],
    'Widespread Dust': [0.3, 0.3, 0.3, 0.3],
    'LightWidespread Dust': [0.4, 0.4, 0.4, 0.4]
}

DISTANCE_SCORE = {
    0: 1.0,
    2: 0.9,
    4: 0.8,
    6: 0.7,
    8: 0.6,
    10: 0.5,
    12: 0.4,
    14: 0.3,
    16: 0.2,
    18: 0.1,
    20: 0.0
}


def temperatureScore(x):
    return -3.044 * (10 ** -8) * (x ** 4) + 3.81 * (10 ** -6) * (x ** 3) - 0.00028 * (x ** 2) + 0.028 * x - 0.17


def dew_point_formula(x):
    return -0.00036 * (x ** 2) + 0.04056 * x - 0.144


def dew_distance_formula(x):
    return -0.1121 * (10 ** -6) * (x ** 4) + 0.00003 * (x ** 3) - 0.00263 * (x ** 2) + 0.07037 * x + 0.36842


def feels_like_distance(FEELS, TEMP):
    r = abs(FEELS - TEMP)
    r = math.ceil(r / 2.0) * 2
    if r > 20:
        r = 20
    return DISTANCE_SCORE[r]


def dayCalculator(TEMP, FEELS, DEW, CONDITION):
    bad_conditions = list()
    a = temperatureScore(TEMP)
    print("Temperature Score: " + str(a))
    if a < 0.3:
        bad_conditions.append("unfavorable temperature")
    b = feels_like_distance(FEELS, TEMP)
    print("Feels-Like Distance: " + str(b))
    if b < 0.3:
        bad_conditions.append("unfavorable temperature disparity between what it feels like and what it is")
    c = dew_point_formula(DEW)
    print("Dew Point: " + str(c))
    if c < 0.3:
        bad_conditions.append("unfavorable dew point")
    d = dew_distance_formula(TEMP - DEW)
    print("Dew Point Distance: " + str(d))
    if d < 0.3:
        bad_conditions.append("unfavorable humidity disparity")
    e = WEATHER_SCORE[CONDITION][whatSeason()]
    print("Season Condition: " + str(e))
    if e < 0.3:
        bad_conditions.append("unfavorable weather conditions")
    score = a * b * c * d * e
    evaluation = None
    if score >= 0.9:
        evaluation = random.choice(GREAT)
    elif (score < 0.9) and (score >= 0.5):
        evaluation = random.choice(GOOD)
    elif (score < 0.5) and (score >= 0.3):
        evaluation = random.choice(OKAY)
    else:
        evaluation = random.choice(BAD)
    return evaluation, bad_conditions


def newDailyReport():
    data = getWeatherJSON('current')
    observation_time = datetime.fromtimestamp(
        email.Utils.mktime_tz(email.Utils.parsedate_tz(data['current_observation']['observation_time_rfc822'])))
    observation_time = observation_time.strftime("%I:%M %p")
    conditions = data['current_observation']['weather']
    feels_like = float(data['current_observation']['feelslike_f'])
    temp = float(data['current_observation']['temp_f'])
    data = getWeatherJSON('forecast')
    high = int(data['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'])
    low = int(data['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'])
    if feels_like < temp:
        weather_string = "Though the temperature is " + str(temp) + ", it feels like " + str(
            feels_like) + " degrees.  It's expected to reach " + str(high) + " today, with a low of " + str(low) + "."
    else:
        weather_string = "The temperature is " + str(temp) + " degrees, with a high of " + str(
            high) + " and a low of " + str(low) + "."
    weather_segment = "As of " + str(observation_time) + " it is currently " + conditions + ". " + weather_string
    dew = dewPointAverage(getWeatherJSON('hourly'))
    day_score, bad_conditions = dayCalculator(temp, feels_like, dew, conditions)
    return day_score, bad_conditions, weather_segment


def dewPointAverage(data):
    dewList = list()
    for d in data['hourly_forecast']:
        dewList.append(int(d['dewpoint']['english']))
    return sum(dewList) / len(dewList)


# def dailyReport():
#     data = getWeatherJSON('current')
#
#     conditions = data['current_observation']['weather']
#
#     feels_like = data['current_observation']['feelslike_f']
#     temp = data['current_observation']['temp_f']
#
#     observation_time = datetime.fromtimestamp(
#         email.Utils.mktime_tz(email.Utils.parsedate_tz(data['current_observation']['observation_time_rfc822'])))
#     observation_time = observation_time.strftime("%I:%M %p")
#
#     data = getWeatherJSON('forecast')
#
#     high = data['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
#     low = data['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
#
#     if feels_like < temp:
#         temperature_string = "Though the temperature is " + str(temp) + ", it feels like " + str(
#             feels_like) + " degrees.  It's expected to reach " + str(high) + " today, with a low of " + str(low) + "."
#     else:
#         temperature_string = "The temperature is " + str(temp) + " degrees, with a high of " + str(
#             high) + " and a low of " + str(low) + "."
#
#     fullReport = "As of " + str(observation_time) + " it is currently " + conditions + ". " + temperature_string
#     saiff(fullReport, "/tmp/DailyReport.aiff")


def getWeatherJSON(weather_type):
    if weather_type == 'current':
        url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/conditions/q/MA/waltham.json"
    if weather_type == 'forecast':
        url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/forecast/q/MA/waltham.json"
    if weather_type == 'astronomy':
        url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/astronomy/q/MA/waltham.json"
    if weather_type == 'hourly':
        url = "http://api.wunderground.com/api/" + WUNDERGROUND_KEY + "/hourly/q/MA/waltham.json"
    agent = MyOpener()
    page = agent.open(url)
    jsonurl = page.read()
    data = json.loads(jsonurl)
    return data


def getSunsetDTO():
    data = getWeatherJSON('astronomy')
    h = data['sun_phase']['sunset']['hour']
    m = data['sun_phase']['sunset']['minute']
    t = datetime.now().replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    t = t - timedelta(minutes=40)
    return t
