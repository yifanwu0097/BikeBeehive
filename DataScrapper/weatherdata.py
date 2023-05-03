import traceback
from weatherScrapper import weatherScrapper

# run forever...
while True:
    try:
        weatherScrapper()
        print("Finished populating current weather data.")

    except:
        print(traceback.format_exc())
