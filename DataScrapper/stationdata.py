import traceback
from staticStation import staticStation
from stationScrapper import stationScrapper

# run once
#staticStation()

# run forever...

try:
    stationScrapper()
    print("Finished populating dynamic station data.")
except:
    # if there is any problem, print the traceback
    print(traceback.format_exc())
