import traceback
from staticStation import staticStation
from stationScrapper import stationScrapper
from weatherForeScrapper import weatherForeScrapper
from weatherScrapper import weatherScrapper

# run once
staticStation()

# run forever...

while True:
    try:
        weatherForeScrapper()
        stationScrapper()
        weatherScrapper()

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())


