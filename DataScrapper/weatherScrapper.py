import requests
import json
import time
from createdbtable import cursor, connection
import datetime as dt

# Weather API keys
WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"
WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,hourly,alerts"
WEATHER_FORE_URI = "https://api.openweathermap.org/data/2.5/onecall?"


def weatherScrapper():
    # DYNAMIC DATA
    # Get the weather dynamic data and load into json
    r_w = requests.get(WEATHER_URI + "&appid=" + WEATHER_APIKEY)
    c_w = json.loads(r_w.text)

    # Populate json weather data into database
    cwvals = (dt.datetime.fromtimestamp(int(c_w['current']['dt'])),
              dt.datetime.fromtimestamp(c_w["current"]["sunrise"]),
              dt.datetime.fromtimestamp(c_w["current"]["sunset"]),
              float(c_w["current"]["temp"]),
              float(c_w["current"]["feels_like"]),
              int(c_w["current"]["pressure"]),
              int(c_w["current"]["humidity"]),
              float(c_w["current"]["uvi"]),
              int(c_w["current"]["clouds"]),
              int(c_w["current"]["visibility"]),
              float(c_w["current"]["wind_speed"]),
              int(c_w["current"]["wind_deg"]),
              c_w["current"]["weather"][0]["description"],
              float(c_w["daily"][0]["temp"]["min"]),
              float(c_w["daily"][0]["temp"]["max"]))

    # Populate weather data into database
    dublinweathersql = """INSERT INTO db_bikes.dublin_new_weather VALUES("%s","%s","%s",%f,%f,%i,%i,%f,%i,%i,%f,%i,"%s",%f,%f);""" % cwvals
    
    cursor.execute(dublinweathersql)
    connection.commit()

    # use cron for keeping running
    time.sleep(5 * 60)
