import traceback
from weatherScrapper import weatherScrapper

# run forever...

while True:
    try:
        # weatherForeScrapper()
        weatherScrapper()
        print("Finished populating current weather data.")

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
