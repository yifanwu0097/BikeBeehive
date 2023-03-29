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
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM db_bikes.station_info")
            station_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return jsonify(station_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/weather")
def get_weather():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM db_bikes.dublin_weather")
            weather_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        if not weather_data:
            weatherScrapper()
            cursor.execute("SELECT * FROM db_bikes.dublin_weather")
            weather_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/weather_forecast")
def get_weather_forecast():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM db_bikes.future_weather_forecast")
            forecast_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        if not forecast_data:
            weatherForeScrapper()
            cursor.execute("SELECT * FROM db_bikes.future_weather_forecast")
            forecast_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return jsonify(forecast_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/hourly_occupancy")
def api_hourly_occupancy():
    try:
        station_id = request.args.get("station_id")
        occupancy = get_hourly_occupancy(station_id)
        return jsonify(occupancy)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "The requested URL was not found on the server."}), 404

if __name__ == "__main__":
    app.run() # it's recommended to not run in debug mode when deploying to production server
