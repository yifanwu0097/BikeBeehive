# Dublin Bikes Web Application
## Team members
- Yifan Wu: https://github.com/yifanwu0097
- Yuanjun Du: https://github.com/yuanjundu
- Shanie Wang: https://github.com/kylinwang318
## Description
This web application displays real-time availability data for all Dublin Bikes stations.Additionally, the application can predict the availability level for each station at a given future time point. With this information, users can easily plan their bike rides and make informed decisions about which stations to use.
## User Guide
- The map displays markers for each Dublin Bikes station, with the color of each marker representing the current availability status of the station. A red marker indicates that there are more bikes available than stands, while a green marker indicates the opposite.
- Clicking on a marker will display detailed information about the selected station. This includes whether the station is currently open, the number of available bikes and stands, whether credit card payments are accepted, and charts showing the average bike availability per hour over a day / per day over a week. 
- The left panel of the page is a form where users can search the bike availability condition of their departure and destination station. Users should input their departure date and time, after clicking the submit button, a pop-up box will appear to display information on both stations’ availability.  If their departure time is within one hour, then the text box will display the current availability. If the departure time is between one hour to 48 hours, then it will display the predicted availability.
- Click the “get current location” button on the top of the map, the centre of map will switch to the user’s current location to help find the nearest station with available bikes or stands.
## Installation
This web application can be downloaded and run using:
- '$ git clone https://github.com/yifanwu0097/Dublin-Bikes-Project.git'
- '$ cd Dublin-Bikes-Project/Flask'
- '$ python app.py'
