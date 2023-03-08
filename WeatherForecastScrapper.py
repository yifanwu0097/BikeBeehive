import requests
import json
import traceback
import time
from datetime import datetime
import sqlalchemy as sqla

WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"

#just to test whether scrapper and database connection work well
#lat = 53.349562
#lon = -6.278198
WEATHER_URI = "https://api.openweathermap.org/data/2.5/onecall?"

# Create table weather containing weather forecast information
def create_table():
    createsttsql = """
    CREATE TABLE IF NOT EXISTS weather_forecast(
    lat DOUBLE,
    lon DOUBLE,
    hourly_dt VARCHAR(255),
    hourly_temp DOUBLE,
    hourly_feels_like DOUBLE,
    hourly_pressure INTEGER,
    hourly_humidity INTEGER,
    hourly_dew_point DOUBLE,
    hourly_uvi DOUBLE,
    hourly_clouds INTEGER,
    hourly_visibility INTEGER,
    hourly_wind_speed DOUBLE,
    hourly_wind_deg INTEGER,
    hourly_wind_gust DOUBLE,
    hourly_weather_description VARCHAR(255),
    hourly_pop DOUBLE,
    daily_dt VARCHAR(255),
    daily_sunrise INTEGER,
    daily_sunset INTEGER,
    daily_temp_min DOUBLE,
    daily_temp_max DOUBLE,
    daily_pressure INTEGER,
    daily_humidity INTEGER,
    daily_dew_point DOUBLE,
    daily_wind_speed DOUBLE,
    daily_wind_deg INTEGER,
    daily_wind_gust DOUBLE,
    daily_weather_description VARCHAR(255),
    daily_clouds INTEGER,
    daily_pop DOUBLE,
    daily_rain DOUBLE,
    daily_uvi DOUBLE
    )"""

    try:
        res = conn.execute(sqla.text("DROP TABLE IF EXIST weather_forecast"))
        res = conn.execute(sqla.text(createsttsql))
        print(res.fetchall())
    except Exception as e:
        print(e)

def write_to_db(text):
    future_weather = json.loads(text)

    for f_w in future_weather:
        vals=(float(f_w["lat"]),
              float(f_w["lon"]),
              f_w["hourly"]["dt"],
              float(f_w["hourly"]["temp"]),
              float(f_w["hourly"]["feels_like"]),
              int(f_w["hourly"]["pressure"]),
              int(f_w["hourly"]["humidity"]),
              float(f_w["hourly"]["dew_point"]),
              float(f_w["hourly"]["uvi"]),
              int(f_w["hourly"]["clouds"]),
              int(f_w["hourly"]["visibility"]),
              float(f_w["hourly"]["wind_speed"]),
              int(f_w["hourly"]["wind_deg"]),
              float(f_w["hourly"]["wind_gust"]),
              f_w["hourly"]["weather"]["description"],
              float(f_w["hourly"]["pop"]),
              f_w["daily"]["dt"],
              int(f_w["daily"]["sunrise"]),
              int(f_w["daily"]["sunset"]),
              float(["daily"]["temp"]["min"]),
              float(["daily"]["temp"]["max"]),
              int(f_w["daily"]["pressure"]),
              int(f_w["daily"]["humidity"]),
              float(f_w["daily"]["dew_point"]),
              float(f_w["daily"]["wind_speed"]),
              int(f_w["daily"]["wind_deg"]),
              float(f_w["daily"]["wind_gust"]),
              f_w["daily"]["weather"]["description"],
              int(f_w["daily"]["clouds"]),
              float(["daily"]["pop"]),
              float(f_w["daily"]["rain"]),
              float(f_w["daily"]["uvi"])
              )
        conn.execute(sqla.text("""INSERT INTO dbbikes.weather_forecast VALUES(%f,%f,"%s",%f,%f,%i,%i,%f,%f,%i,%i,%f,%i,%f,"%s",%f,"%s",%i,%i,%f,%f,%i,%i,%f,%f,%i,%f,"%s",%i,%f,%f,%f);""" % vals))
        conn.commit()

create_table()

try:
    stations = json.loads("dublin.json")
    for station in stations:
        lat = station["latitude"]
        lon = station["longtitude"]

    r = requests.get(WEATHER_URI + "lat=" + str(lat) + "&lon=" + str(lon) + "&exclude=current,minutely,alerts" + "&appid=" + WEATHER_APIKEY)
    #print(json.loads(r.text))

    write_to_db(r.text)

    # now sleep for 5 minutes
    
except:
    # if there is any problem, print the traceback
    print(traceback.format_exc())