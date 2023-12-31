from flask import Flask, jsonify, render_template
import pymysql.cursors
import requests
import pickle
import datetime as dt

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = 3306
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,alerts&appid=f0d90ef7fcc8781efadf746287963079"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stations")
def stations():
    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
    with conn.cursor() as cursor:
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
    conn.close()
    return jsonify(stations_data)

@app.route("/hourly/<int:station_id>")
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
    conn.close()
    return jsonify(hourly_availability_data)


@app.route("/daily/<int:station_id>")
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
    conn.close()
    return jsonify(daily_availability_data)


@app.route("/prediction/<int:station_id>/<int:day_num>/<int:future_hour>")
def get_prediction(station_id, day_num, future_hour):
    # day_num starts from Sun
    weekdays = ['weekday_Sunday','weekday_Monday','weekday_Tuesday','weekday_Wednesday','weekday_Thursday','weekday_Friday','weekday_Saturday']
    current_hour = dt.datetime.now().hour
    if current_hour <= future_hour:
        index = future_hour - current_hour
    else:
        index = 24 - current_hour + future_hour
    with open('MachineLearning/model_{}.pkl'.format(station_id),'rb') as handle:
        model = pickle.load(handle)
        features = ['weekday_Sunday','weekday_Monday','weekday_Tuesday','weekday_Wednesday','weekday_Thursday','weekday_Friday','weekday_Saturday','hour','temp','clouds','wind_speed','pressure','humidity']
        
        hourly_forecast = weather_hourly_forecast()
        target_forcast = hourly_forecast[index]
        input = [0] * len(features)
        input[features.index('hour')] = future_hour
        input[features.index('temp')] = target_forcast['temp']
        input[features.index('clouds')] = target_forcast['clouds']
        input[features.index('wind_speed')] = target_forcast['wind_speed']
        input[features.index('pressure')] = target_forcast['pressure']
        input[features.index('humidity')] = target_forcast['humidity']
        input[features.index(weekdays[day_num])] = 1
        prediction = model.predict([input])
    return list(prediction)

@app.route("/weather")
def current_weather():
    response = requests.get(WEATHER_URI).json()
    current_weather = response['current']
    return current_weather

@app.route("/forecast/daily")
def weather_daily_forecast():
    response = requests.get(WEATHER_URI).json()
    daily_forecast = response['daily']
    return daily_forecast

@app.route("/forecast/hourly")
def weather_hourly_forecast():
    response = requests.get(WEATHER_URI).json()
    hourly_forecast = response['hourly']
    return hourly_forecast

@app.route("/predictions/<int:station_id>")
def get_predictions(station_id):
    weekdays = ['weekday_Sunday','weekday_Monday','weekday_Tuesday','weekday_Wednesday','weekday_Thursday','weekday_Friday','weekday_Saturday']
    current_hour = dt.datetime.now().hour
    current_day = dt.datetime.now().weekday() + 1 
    if current_day == 7:
        current_day = 0
    with open('MachineLearning/model_{}.pkl'.format(station_id),'rb') as handle:
        model = pickle.load(handle)
        features = ['weekday_Sunday','weekday_Monday','weekday_Tuesday','weekday_Wednesday','weekday_Thursday','weekday_Friday','weekday_Saturday','hour','temp','clouds','wind_speed','pressure','humidity']
        hourly_forecasts = weather_hourly_forecast()
        i = 1
        predictions = []
        for hourly_forecast in hourly_forecasts:
            input = [0] * len(features)
            input[features.index('hour')] = current_hour + i
            input[features.index('temp')] = hourly_forecast['temp']
            input[features.index('clouds')] = hourly_forecast['clouds']
            input[features.index('wind_speed')] = hourly_forecast['wind_speed']
            input[features.index('pressure')] = hourly_forecast['pressure']
            input[features.index('humidity')] = hourly_forecast['humidity']
            
            if current_day < 5:
                if i < 24 - current_hour:
                    input[features.index(weekdays[current_day])] = 1
                elif 24 - current_hour <= i < 48 - current_hour:
                    input[features.index(weekdays[current_day+1])] = 1
                else:
                    input[features.index(weekdays[current_day+2])] = 1
            elif current_day == 5:
                if i < 24 - current_hour:
                    input[features.index(weekdays[current_day])] = 1
                elif 24 - current_hour <= i < 48 - current_hour:
                    input[features.index(weekdays[current_day+1])] = 1
                else:
                    input[features.index(weekdays[0])] = 1
            elif current_day == 6:
                if i < 24 - current_hour:
                    input[features.index(weekdays[current_day])] = 1
                elif 24 - current_hour <= i < 48 - current_hour:
                    input[features.index(weekdays[0])] = 1
                else:
                    input[features.index(weekdays[1])] = 1
            prediction = model.predict([input])
            predictions.append(list(prediction)[0])
            i += 1
    return predictions

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
