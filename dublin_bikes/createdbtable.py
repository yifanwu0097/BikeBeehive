import sqlalchemy as sqla

URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

engine = sqla.create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# Create the database dbbikes
sql = """
CREATE DATABASE IF NOT EXISTS dbbikes;
"""
conn = engine.connect()
result = conn.execute(sqla.text(sql))
print(result)


# Create table use a function
def createtable(sqlsyntax):
    try:
        res = conn.execute(sqla.text(sqlsyntax))
        print(res.fetchall())
    except Exception as e:
        print(e)


# Create static data table containing dublin station information
createstaticsql = """
CREATE TABLE IF NOT EXISTS dublin(
number INTEGER,
name VARCHAR(255),
address VARCHAR(255),
latitude REAL,
longitude REAL)"""
createtable(createstaticsql)

# Create table station containing station information
createsttsql = """
CREATE TABLE IF NOT EXISTS station(
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
CREATE TABLE IF NOT EXISTS availability(
number INTEGER,
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update INTEGER)
"""
createtable(createavtsql)

# Create table weather containing weather information now
createwthsql = """
CREATE TABLE IF NOT EXISTS weather(
dt INTEGER(255),
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
createtable(createwthsql)

# Create table weather_forecast containing future weather forecast information
createfwthsql = """
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
    daily_uvi DOUBLE
    )"""

createtable(createfwthsql)
