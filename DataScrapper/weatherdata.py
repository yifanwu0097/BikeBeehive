import traceback
from weatherScrapper import weatherScrapper

# run forever...

while True:
    try:
        # weatherForeScrapper()
        weatherScrapper()

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
