import requests
import json
import time
import datetime
import sqlalchemy as sqla
from createdbtable import conn

# Station API keys
JCKEY = "3963133e057b9124ba668c500c291bb165933b46"
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations?"


def stationScrapper():
    # Station and Availability
    # Get the stations dynamic data and load into json
    now = datetime.datetime.now()
    r_sa = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
    stations = json.loads(r_sa.text)

    # Write station dynamic data into stationinfo.txt for test
    with open("stationinfo.txt".format(now).replace(" ", "_"), "w") as f:
        f.write(r_sa.text)

    # Populate json station and availability data into database
    for station in stations:
        # Get station data in tuple form
        vals = (station.get('address'),
                station.get('banking'),
                int(station.get('bike_stands')),
                int(station.get('bonus')),
                station.get('contract_name'),
                station.get('name'),
                int(station.get('number')),
                float(station.get('position').get('lat')),
                float(station.get('position').get('lng')),
                station.get('status'))

        # Get availability data in tuple form
        avab = (int(station.get('number')),
                int(station.get('available_bikes')),
                int(station.get('available_bike_stands')),
                int(station.get('last_update')))

        # Populate station and availability data into database
        conn.execute(sqla.text("""INSERT INTO dbbikes.station VALUES("%s","%s",%i,%i,"%s","%s",%i,%f,%f,"%s");""" % vals))
        conn.execute(sqla.text("""INSERT INTO dbbikes.availability VALUES(%i, %i, %i, %i);""" % avab))

        conn.commit()

    # now sleep for 5 minutes
    time.sleep(5 * 60)
