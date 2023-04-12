from flask import Flask, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_caching import Cache
import pymysql.cursors
import requests
import json

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = 3306
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"
# conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://picto:Comp30830@database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com:3306/dbbikes"
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# db = SQLAlchemy(app)
# cache = Cache(app)


@app.route("/")
# @cache.cached()
def index():
    return render_template('index.html')

# Display all stations info


@app.route("/stations")
# @cache.cached()
def stations():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        # select and show all of the stations without showing its occupancy
        # sql_static = """

        #     """
        # cursor.execute(sql_static)

        sql = """
            SELECT d.number, d.name, d.address, d.position_lat, d.position_lng, d.banking, d.status, a.available_bikes, a.available_bike_stands, a.last_update
            FROM (
                SELECT * FROM db_bikes.station_info LIMIT 114
            ) as d
            JOIN db_bikes.station_new_availability as a
            ON d.number = a.number
            WHERE (a.number, a.last_update) 
            IN (SELECT number, MAX(last_update) FROM db_bikes.station_new_availability 
            GROUP BY number)
            ORDER BY number DESC;
            """
        cursor.execute(sql)
        stations_data = [dict(zip([column[0] for column in cursor.description], row))
                         for row in cursor.fetchall()]
    return jsonify(stations_data)


# Display selected station's availability

# TODO: is this route necessary?
@app.route("/availability/<int:station_id>")
# @cache.cached()
def get_availability():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
            SELECT s.name, a.last_update, a.available_bikes, a.available_bike_stands
            FROM db_bikes.station_info as s
            JOIN db_bikes.station_new_availability as a
            ON s.number = a.number
            WHERE s.number = {station_number}
            AND (a.number, a.last_update) 
                        IN (SELECT number, MAX(last_update) FROM db_bikes.station_new_availability 
                        GROUP BY number)
            GROUP BY s.name, a.last_update
            ORDER BY s.name, a.last_update desc;
        """
        cursor.execute(sql)
        availability_data = cursor.fetchall()

    return json.dumps(availability_data)

@app.route("/hourly/<int:station_id>")
# @cache.cached()
def get_hourly_availability(station_id):
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT avg(available_bikes), avg(available_bike_stands), 
        (MOD(EXTRACT(HOUR FROM last_update) + CASE WHEN last_update > '2023-03-26 01:00:00' THEN 1 ELSE 0 END, 24)) as hour
        FROM db_bikes.station_new_availability
        WHERE number = {}
        GROUP BY hour
        ORDER BY hour;
        """.format(station_id)
        cursor.execute(sql)
        hourly_availability_data = cursor.fetchall()
    return jsonify(hourly_availability_data)


@app.route("/daily/<int:station_id>")
# @cache.cached()
def get_daily_availability(station_id):
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT avg(available_bikes), avg(available_bike_stands), 
        WEEKDAY(last_update) as weekday
        FROM db_bikes.station_new_availability
        WHERE number = {}
        GROUP BY weekday
        ORDER BY weekday;
        """.format(station_id)
        cursor.execute(sql)
        daily_availability_data = cursor.fetchall()

    return jsonify(daily_availability_data)

@app.route("/weather")
# @cache.cached()
def current_weather():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT (temp - 273.15) as celsius_temp, (feels_like - 273.15) as celsius_feels_like, weather_description, (temp_min - 273.15) as celsius_temp_min, (temp_max - 273.15) as celsius_temp_max
        FROM db_bikes.dublin_new_weather 
        ORDER BY dt DESC
        LIMIT 1;
        """
        cursor.execute(sql)
        current_weather = cursor.fetchall()
        print(current_weather)

    return jsonify(current_weather)

# TODO: call weather forecast based on bike station location
@app.route("/forecast/<int:station_id>")
def weather_forecast():
    conn = pymysql.connect(host=URI, user=USER,
                           password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
        sql = """
        SELECT (temp - 273.15) as celsius_temp, (feels_like - 273.15) as celsius_feels_like, weather_description, (temp_min - 273.15) as celsius_temp_min, (temp_max - 273.15) as celsius_temp_max
        FROM db_bikes.dublin_new_weather 
        ORDER BY dt DESC
        LIMIT 1;
        """
        cursor.execute(sql)
        weather_forecast = cursor.fetchall()

    return json.dumps(weather_forecast)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
