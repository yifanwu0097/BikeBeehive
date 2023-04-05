from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import pymysql.cursors
import requests
import json

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = 3306
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://picto:Comp30830@database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com:3306/dbbikes"
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# db = SQLAlchemy(app)
cache = Cache(app)

@app.route("/")
@cache.cached()
def index():
    return render_template('index.html')

# Display all stations info
@app.route("/stations")
@cache.cached()
def stations():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT s.number, s.name, s.address, s.position_lat, s.position_lng, a.available_bikes, a.available_bike_stands, MAX(a.last_update)
        FROM db_bikes.station_info as s
        JOIN db_bikes.station_new_availability as a
        ON s.number = a.number
        GROUP BY s.name, time
        ORDER BY s.name, time;
        """
        cursor.execute(sql)
        stations_data = cursor.fetchall()

    return json.dumps(stations_data)

# Display selected station's availability
@app.route("/availability/<int:station_id>")
@cache.cached()
def get_availability():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT s.name, a.last_update as time, a.available_bikes, a.available_bike_stands
        FROM db_bikes.station_info as s
        JOIN db_bikes.station_new_availability as a
        ON s.number = a.number
        WHERE s.number = {station_id}
        GROUP BY s.name, time
        ORDER BY s.name, time;
        """
        cursor.execute(sql)
        availability_data = cursor.fetchall()

    return json.dumps(availability_data)

@app.route("/hourly/<int:station_id>")
@cache.cached()
def get_hourly_availability():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT s.name, a.available_bikes, a.available_bike_stands, EXTRACT(HOUR FROM last_update) as hourly
        FROM db_bikes.station_info as s
        JOIN db_bikes.station_new_availability as a
        ON s.number = a.number
        WHERE s.number = {station_id}
        GROUP BY s.name, time
        ORDER BY s.name, time;
        """
        cursor.execute(sql)
        availability_data = cursor.fetchall()

    return json.dumps(availability_data)


@app.route("/weather_forecast")
@cache.cached()
def weather_forecast():
    WEATHER_APIKEY = "f0d90ef7fcc8781efadf746287963079"
    WEATHER_FORE_URI = "https://api.openweathermap.org/data/2.5/onecall?" 
    response = requests.get(WEATHER_FORE_URI + "lat=53.3498" + "&lon=-6.2603"
         + "&exclude=current,minutely,alerts" + "&appid=" + WEATHER_APIKEY).json()
    # wait to be finalised

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)








    

    
    
