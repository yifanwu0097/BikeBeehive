import requests
import json
import traceback
import time
import datetime
import sqlalchemy as sqla
from createdbtable import conn


JCKEY = "3963133e057b9124ba668c500c291bb165933b46"
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations?"

# collect station availability

# run forever...
while True:
    try:
        now = datetime.datetime.now()
        r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
        stations = json.loads(r.text)

        # Write the information into stationinfo.txt
        with open("stationinfo.txt".format(now).replace(" ", "_"), "w") as f:
            f.write(r.text)

        # Load data into database
        print(type(stations), len(stations))
        for station in stations:
            print(station)
            vals = (station.get('address'), station.get('banking'), int(station.get('bike_stands')),
                    int(station.get('bonus')), station.get('contract_name'), station.get('name'), int(station.get('number')),
                    float(station.get('position').get('lat')), float(station.get('position').get('lng')), station.get('status'))
            print(vals)

            avab = (int(station.get('number')), int(station.get('available_bikes')), int(station.get('available_bike_stands')), int(station.get('last_update')))
            print(avab)

            conn.execute(sqla.text("""INSERT INTO dbbikes.station VALUES("%s","%s",%i,%i,"%s","%s",%i,%f,%f,"%s");""" % vals))
            conn.execute(sqla.text("""INSERT INTO dbbikes.availability VALUES(%i, %i, %i, %i);""" % avab))
            conn.commit()
            print("\n")

        # now sleep for 5 minutes
        time.sleep(5 * 60)

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())


