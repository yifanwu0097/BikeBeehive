import requests
import json
import pymysql.cursors
from createdbtable import cursor, connection

# Weather API keys
WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"
WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,hourly,alerts"
WEATHER_FORE_URI = "https://api.openweathermap.org/data/2.5/onecall?"


def weatherForeScrapper():
    # DYNAMIC DATA
    # Test the input position to get the weather forecast
    lat = input("Input the latitude: ")
    lon = input("Input the longitude: ")

    r_wf = requests.get(WEATHER_FORE_URI + "lat=" + lat + "&lon=" + lon
         + "&exclude=current,minutely,alerts" + "&appid=" + WEATHER_APIKEY)

    # Populate json weather data into database
    f_w = json.loads(r_wf.text)
    cwfvals = (float(f_w["lat"]),
               float(f_w["lon"]),
               f_w["hourly"][0]["dt"],
               float(f_w["hourly"][0]["temp"]),
               float(f_w["hourly"][0]["feels_like"]),
               int(f_w["hourly"][0]["pressure"]),
               int(f_w["hourly"][0]["humidity"]),
               float(f_w["hourly"][0]["dew_point"]),
               float(f_w["hourly"][0]["uvi"]),
               int(f_w["hourly"][0]["clouds"]),
               int(f_w["hourly"][0]["visibility"]),
               float(f_w["hourly"][0]["wind_speed"]),
               int(f_w["hourly"][0]["wind_deg"]),
               float(f_w["hourly"][0]["wind_gust"]),
               f_w["hourly"][0]["weather"][0]["description"],
               float(f_w["hourly"][0]["pop"]),
               f_w["daily"][0]["dt"],
               int(f_w["daily"][0]["sunrise"]),
               int(f_w["daily"][0]["sunset"]),
               float(f_w["daily"][0]["temp"]["min"]),
               float(f_w["daily"][0]["temp"]["max"]),
               int(f_w["daily"][0]["pressure"]),
               int(f_w["daily"][0]["humidity"]),
               float(f_w["daily"][0]["dew_point"]),
               float(f_w["daily"][0]["wind_speed"]),
               int(f_w["daily"][0]["wind_deg"]),
               float(f_w["daily"][0]["wind_gust"]),
               f_w["daily"][0]["weather"][0]["description"],
               int(f_w["daily"][0]["clouds"]),
               float(f_w["daily"][0]["pop"]),
               float(f_w["daily"][0]["uvi"])
               )

    # Populate weather forecast data into database
    weatherforecastsql = """INSERT INTO db_bikes.future_weather_forecast 
                            VALUES(%f,%f,"%s",%f,%f,%i,%i,%f,%f,%i,%i,%f,%i,%f,"%s",%f,"%s",%i,%i,%f,%f,%i,%i,%f,%f,%i,%f,"%s",%i,%f,%f);"""% cwfvals
    cursor.execute(weatherforecastsql)
    connection.commit()
