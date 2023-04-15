import requests
import json
import datetime as dt

WEATHER_URI = "https://api.openweathermap.org/data/3.0/onecall?lat=53.3498&lon=-6.2603&exclude=minutely,alerts&appid=f0d90ef7fcc8781efadf746287963079"
response = requests.get(WEATHER_URI).json()
hourly_forecast = response['hourly']
daily_forecast = response['daily']
current = response['current']
print(daily_forecast)