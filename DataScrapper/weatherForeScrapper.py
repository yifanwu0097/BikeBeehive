import requests
import json
import pymysql.cursors
from createdbtable import cursor, connection
import datetime as dt

# Weather API keys
WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"
WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,hourly,alerts"
WEATHER_FORE_URI = "https://api.openweathermap.org/data/2.5/forcast?lat=53.3498&lon=-6.260"

def weatherForeScrapper():
    # DYNAMIC DATA
    # Test the input position to get the weather forecast

    r_wf = requests.get(WEATHER_FORE_URI + "&exclude=current,minutely,alerts" + "&appid=" + WEATHER_APIKEY)

    # Populate json weather data into database
    f_w = json.loads(r_wf.text)
    cwfvals = (float(f_w["lat"]),
               float(f_w["lon"]),
               dt.datetime.fromtimestamp(f_w["hourly"][0]["dt"]),
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
               dt.datetime.fromtimestamp(int(f_w["daily"][0]["sunrise"])),
               dt.datetime.fromtimestamp(int(f_w["daily"][0]["sunset"])),
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
    print(cwfvals)

    # Populate weather forecast data into database
    weatherforecastsql = """INSERT INTO dbbikes.future_weather_forecast 
                            # VALUES(%f,%f,"%s",%f,%f,%i,%i,%f,%f,%i,%i,%f,%i,%f,"%s",%f,"%s","%s","%s",%f,%f,%i,%i,%f,%f,%i,%f,"%s",%i,%f,%f);"""% cwfvals
    cursor.execute(weatherforecastsql)
    connection.commit()


