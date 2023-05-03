import traceback
from stationScrapper import stationScrapper

# run once
#staticStation()

# run forever...
while True:
    try:
        stationScrapper()
        print("Finished populating dynamic station data.")
    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
