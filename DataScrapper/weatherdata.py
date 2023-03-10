import traceback
import cronitor
cronitor.api_key = 'c2d3a43ef9c7406c8dfb624ce09fc256'
from weatherScrapper import weatherScrapper

# run forever...

cronitor.Monitor.put(
    key='background-weather-scrapper',
    type='job',
    schedule='*/30 * * * *'
)

while True:
    try:
        # weatherForeScrapper()
        monitor = cronitor.Monitor('background-weather-scrapper')
        weatherScrapper()
        monitor.ping(state='run')
        monitor.ping(state='complete')
        monitor.ping(state='fail')

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())