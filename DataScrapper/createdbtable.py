import pymysql.cursors

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = 3306
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

connection = pymysql.connect(host=URI, user=USER, password=PASSWORD, port=PORT, database=DB)
cursor = connection.cursor()

# Create the database db_bikes
sql = """
CREATE DATABASE IF NOT EXISTS db_bikes;
"""
cursor.execute(sql)
print("Database is created.")


# Create table use a function
def createtable(sqlsyntax):
    try:
        print(sqlsyntax)
        cursor.execute(sqlsyntax)
        print("Table is created.")
    except Exception as e:
        print(e)


# Create static data table containing dublin station information
createstaticsql = """
CREATE TABLE IF NOT EXISTS db_bikes.dublin_station(
number INTEGER,
name VARCHAR(255),
address VARCHAR(255),
latitude REAL,
longitude REAL)"""
createtable(createstaticsql)

# Create table station containing station information
createsttsql = """
CREATE TABLE IF NOT EXISTS db_bikes.station_info(
address VARCHAR(255),
banking VARCHAR(255),
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(255),
name VARCHAR(255),
number INTEGER,
position_lat REAL,
position_lng REAL,
status VARCHAR(255)
)"""
createtable(createsttsql)

# Create table availability containing bikes and bike stands information
createavtsql = """
CREATE TABLE IF NOT EXISTS db_bikes.station_new_availability(
number INTEGER,
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update DateTime)
"""
createtable(createavtsql)

# Create table weather containing weather information now
createwthsql = """
CREATE TABLE IF NOT EXISTS db_bikes.dublin_new_weather(
dt DateTime,
sunrise DateTime,
sunset DateTime,
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
createtable(createwthsql)

# Create table weather_forecast containing future weather forecast information
createfwthsql = """
    CREATE TABLE IF NOT EXISTS db_bikes.future_weather_forecast(
    lat DOUBLE,
    lon DOUBLE,
    hourly_dt DateTime,
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
    daily_sunrise DateTime,
    daily_sunset DateTime,
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
    daily_uvi DOUBLE
    )"""

createtable(createfwthsql)
