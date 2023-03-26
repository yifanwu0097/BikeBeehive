from flask import Flask, render_template, jsonify, request
from createdbtable import connection
from stationScrapper import get_hourly_occupancy
from weatherScrapper import weatherScrapper
from weatherForeScrapper import weatherForeScrapper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stations")
def get_stations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM db_bikes.station_info")
        station_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return jsonify(station_data)

@app.route("/api/weather")
def get_weather():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM db_bikes.dublin_weather")
        weather_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    if not weather_data:
        weatherScrapper()
        cursor.execute("SELECT * FROM db_bikes.dublin_weather")
        weather_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return jsonify(weather_data)

@app.route("/api/weather_forecast")
def get_weather_forecast():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM db_bikes.future_weather_forecast")
        forecast_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    if not forecast_data:
        weatherForeScrapper()
        cursor.execute("SELECT * FROM db_bikes.future_weather_forecast")
        forecast_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return jsonify(forecast_data)

@app.route("/api/hourly_occupancy")
def api_hourly_occupancy():
    station_id = request.args.get("station_id")
    occupancy = get_hourly_occupancy(station_id)
    return jsonify(occupancy)

if __name__ == "__main__":
    app.run(debug=True)
