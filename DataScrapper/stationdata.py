import traceback
from stationScrapper import stationScrapper

# run once
# staticStation()

# run forever...

while True:
    try:
        stationScrapper()

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
