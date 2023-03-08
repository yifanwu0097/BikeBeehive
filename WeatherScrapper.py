import requests
import json
import traceback
import time
from datetime import datetime
import sqlalchemy as sqla

WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"
WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,hourly,alerts&appid=f0d90ef7fcc8781efadf746287963079"

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

engine = sqla.create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# Create table weather containing current weather information
def create_table():
    createsttsql = """
    CREATE TABLE IF NOT EXISTS weather(
    dt VARCHAR(255),
    sunrise VARCHAR(255),
    sunset VARCHAR(255),
    temp DOUBLE,
    feels_like DOUBLE,
    pressure INTEGER,
    humidity INTEGER,
    uvi DOUBLE,
    clouds INTEGER,
    visibility INTEGER,
    wind_speed DOUBLE,
    wind_deg INTEGER,
    weather_description VARCHAR(255),
    temp_min DOUBLE,
    temp_max DOUBLE
    )"""

    try:
        res = conn.execute(sqla.text("DROP TABLE IF EXIST weather"))
        res = conn.execute(sqla.text(createsttsql))
        print(res.fetchall())
    except Exception as e:
        print(e)

def write_to_db(text):
    current_weather = json.loads(text)

    for c_w in current_weather:
        vals = (c_w["current"]["dt"],
                c_w["current"]["sunrise"],
                c_w["current"]["sunset"],
                float(c_w["current"]["temp"]),
                float(c_w["current"]["feels_like"]),
                int(c_w["current"]["pressure"]),
                int(c_w["current"]["humidity"]),
                float(c_w["current"]["uvi"]),
                int(c_w["current"]["clouds"]),
                int(c_w["current"]["visibility"]),
                float(c_w["current"]["wind_speed"]),
                int(c_w["current"]["wind_deg"]),
                c_w["current"]["weather"]["description"],
                float(c_w["daily"]["temp"]["min"]),
                float(c_w["daily"]["temp"]["max"]))
        conn.execute(sqla.text("""INSERT INTO dbbikes.weather VALUES("%s","%s","%s",%f,%f,%i,%i,%f,%i,%i,%f,%i,"%s",%f,%f);""" % vals))
        conn.commit()

create_table()
# collect dublin weather
# run forever...

while True:
    try:
        r = requests.get(WEATHER_URI + "&appid=" + WEATHER_APIKEY)
        #print(json.loads(r.text))

        write_to_db(r.text)
        # now sleep for 1 hour
        time.sleep(60 * 60)
    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())