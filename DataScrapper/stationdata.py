import traceback
import cronitor
cronitor.api_key = 'c2d3a43ef9c7406c8dfb624ce09fc256'
from stationScrapper import stationScrapper

# run once
# staticStation()

# run forever...

cronitor.Monitor.put(
    key='background-station-scrapper',
    type='job',
    schedule='*/10 * * * *'
)

while True:
    try:
        monitor = cronitor.Monitor('background-station-scrapper')
        stationScrapper()
        monitor.ping(state='run')
        monitor.ping(state='complete')
        monitor.ping(state='fail')

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
