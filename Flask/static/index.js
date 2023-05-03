$(document).ready(function () {
    // click the search button
    $("#submit").on("click", function () {
        $("#station-info").css("display", "block");
    });
    // close the info panel
    $(".close").on("click", function () {
        $("#station-info").css("display", "none");
    });
});

google.charts.load("current", { packages: ["corechart"] });
displayCurrentWeather();
displayForeWeather();
travelInfo();

function travelInfo(){
    fetch('/stations').then(response =>
    response.json()).then(data =>{
        const stationsDict = {};
        for (const station of data){
            stationsDict[station.name] = station.number;
        }
        var form = document.querySelector("form");
        $("#submit").on("click", function(){
            var depStationName = document.getElementById('start-station').value.toUpperCase();
            var desStationName = document.getElementById('end-station').value.toUpperCase();
            var travelDateString = document.getElementById('date').value;
            var travelTimeString = document.getElementById('time').value;

            var depStationId = stationsDict[depStationName];
            var desStationId = stationsDict[desStationName];

            if (!depStationId || !desStationId){
                alert("Please check your input carefully.")
            } else {
                var travelTime = new Date(travelDateString + "T" + travelTimeString);
                var travelHour = travelTime.getHours();

                var travelDay = travelTime.getDay();

                const timeDiff = Math.abs(travelTime.getTime() - new Date().getTime());
                const hoursDiff = Math.floor(timeDiff / (1000*60*60));

                let depName = depStationName.toUpperCase();
                const depNameDiv = document.getElementById("dep-name");
                depNameDiv.innerHTML = depName;
                depData = data.find(item => item.name === depStationName.toUpperCase());
                let desName = desStationName.toUpperCase();
                const desNameDiv = document.getElementById("des-name");
                desNameDiv.innerHTML = desName;
                desData = data.find(item => item.name === desStationName.toUpperCase());

                if (hoursDiff == 0){
                    let depWords = `
                        <p><strong>Status:</strong> ${depData.status}</p>
                        <p><strong>Available bikes:</strong> ${
                            depData.available_bikes
                        }</p>
                        <p><strong>Available stands:</strong> ${
                            depData.available_bike_stands
                        }</p>
                        <p><strong>Credit cards accepted:</strong> ${
                            depData.banking === "True" ? "Yes" : "No"
                        }</p>
                        `;
                    const depWordsDiv = document.getElementById("dep-words");
                    depWordsDiv.innerHTML = depWords;

                    let desWords = `
                        <p><strong>Status:</strong> ${desData.status}</p>
                        <p><strong>Available bikes:</strong> ${
                            desData.available_bikes
                        }</p>
                        <p><strong>Available stands:</strong> ${
                            desData.available_bike_stands
                        }</p>
                        <p><strong>Credit cards accepted:</strong> ${
                            desData.banking === "True" ? "Yes" : "No"
                        }</p>
                        `;
                    const desWordsDiv = document.getElementById("des-words");
                    desWordsDiv.innerHTML = desWords;
                    drawHourlyChart(depStationId,"dep-chart-1");
                    drawDailyChart(depStationId,"dep-chart-2");
                    drawHourlyChart(desStationId,"des-chart-1");
                    drawDailyChart(desStationId,"des-chart-2");

                } else if (0 < hoursDiff < 48){
                    fetch("/prediction/" + depStationId + "/" + travelDay + "/" + travelHour).then(response => {
                    console.log(response);
                    return response.json();
                }).then(data => {
                    var depData = Math.floor(data[0]);
                    var depWords = "Predicted number of available bikes: " +depData;
                    const depWordsDiv = document.getElementById("dep-words");
                    depWordsDiv.innerHTML = depWords;
                  })
                    drawPredictionChart(depStationId,"dep-chart-1");
                    fetch("/prediction/" + desStationId + "/" + travelDay + "/" + travelHour).then(response => {
                        console.log(response);
                        return response.json();
                    }).then(data => {
                        var desData = Math.floor(data[0]);
                        var desWords = "Predicted number of available bikes: " +desData;
                        const desWordsDiv = document.getElementById("des-words");
                        desWordsDiv.innerHTML = desWords;
                      })
                    drawPredictionChart(desStationId,"des-chart-1");
                }else{
                    alert("Please check your input carefully.");
                }
            }
        });
    });
}

function drawHourlyChart(station_id,location) {
    fetch("/hourly/" + station_id).then((response) => {
        console.log(response);
        return response.json();
    })
    .then((data) => {
        var charData = new google.visualization.DataTable();
        charData.addColumn("number", "Hour of Day");
        charData.addColumn("number", "Available Bikes");
        data.forEach((hourlydata) => {
            charData.addRow([
                hourlydata[2],
                parseFloat(hourlydata[0].toString()),
            ]);
        });
        var options = {
            title: "Hourly Bike Availability",
            hAxis: {
                title: "Hour of the Day",
                ticks: [
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23,
                ],
            },
            vAxis: { title: "Available Bike Number" },
            legend: "none",
            width: "330",
        };
        var hourlyChart = new google.visualization.LineChart(
            document.getElementById(location)
        );
        hourlyChart.draw(charData, options);
    })
        .catch((error) => console.error(error));
}

function drawDailyChart(station_id,location) {
    var weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    fetch("/daily/" + station_id).then((response) => {
        console.log(response);
        return response.json();
      })
    .then((data) => {
        var charData = new google.visualization.DataTable();
        charData.addColumn("string", "Day of Week");
        charData.addColumn("number", "Available Bikes");
        data.forEach((dailydata) => {
            charData.addRow([
                weekday[dailydata[2]],
                parseFloat(dailydata[0].toString()),
            ]);
        });
        var options = {
            title: "Daily Bike Availability",
            hAxis: { title: "Day of the Week" },
            vAxis: { title: "Available Bike Number" },
            legend: "none",
            width: "330",
        };
        var dailyChart = new google.visualization.LineChart(
            document.getElementById(location)
        );
        dailyChart.draw(charData, options);
    }).catch((error) => console.error(error));
}

function getPrediction(station_id, day_num, future_hour){
    fetch("/prediction/" + station_id + "/" + day_num + "/" + future_hour).then(response => {
        console.log(response);
        return response.json();
    }).then(data => {
        return Math.floor(data[0]);
    }).catch(error => console.error(error));
}

function getPredictions(station_id){
    fetch("/predictions/"+station_id).then(response=>{
        console.log(response);
        return response.json();
    }).then(data =>{
        return data;
    }).catch(error => console.error(error));
}

function drawPredictionChart(station_id, location){
    fetch("/predictions/"+station_id).then(response => {
        console.log(response);
        return response.json();
    }).then(data => {
        var current_hour = new Date().getHours();
        let hours = [];
        for(let i=1; i<data.length; i++){
            hours.push(current_hour+i);
        }
        var charData = new google.visualization.DataTable();
        charData.addColumn("number", "Future Hours");
        charData.addColumn("number", "Available Bikes");
        data.forEach((predictiondata,i) => {
            charData.addRow([hours[i], predictiondata]);
        });
        var options = {
            title: "Predicted Bike Availability",
            hAxis: { title: "Future Hours" },
            vAxis: { title: "Available Bike Number" },
            legend: "none",
            width: "330",
        };
        var predictionChart = new google.visualization.LineChart(
            document.getElementById(location)
        );
        predictionChart.draw(charData, options);
    })
}

// Fetch stations_data from app.py
fetch("/stations", { mode: "no-cors" }).then((response) => {
    console.log(response);
    (response) => response.json();
}).then((data) => {
    window.stations = data;
}).catch((error) => console.error(error));

// Use jQuery to get stations_data json
var jqxhr = $.getJSON(
    "/stations",
    function (stations) {
        initMap(stations);
    }
)

function initMap(stations) {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 53.349805, lng: -6.26031 },
        zoom: 13,
    });

    let geolocation = new google.maps.InfoWindow();
    const currLocButton = document.createElement("button");
    currLocButton.type = "button";
    currLocButton.textContent = "Get Your Current Location";
    currLocButton.classList.add("location-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(currLocButton);
    currLocButton.addEventListener('click',() => {
        if (navigator.geolocation){
            navigator.geolocation.getCurrentPosition(
                (position)=>{
                    const currLoc = {
                        lat:position.coords.latitude,
                        lng:position.coords.longitude,
                    };
                    geolocation.setPosition(currLoc);
                    geolocation.setContent("You are Here. Find bike stations near you!");
                    geolocation.open(map);
                    map.setCenter(currLoc);
                }, () => {
                    locationErrorHandling(true, geolocation, map.getCenter());
                }
            );
        }else{
            locationErrorHandling(false,geolocation,map.getCenter());
        }
    });
    Object.values(stations).forEach((station) => {
        const color =
        (station.available_bikes / (station.available_bikes + station.available_bike_stands)) * 100 > 50 ?
        "green" : "red";

        const marker = new google.maps.Marker({
            position: new google.maps.LatLng(
                station.position_lat,
                station.position_lng
            ),
            map: map,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: station.available_bikes / 2,
                fillColor: color,
                fillOpacity: 0.8,
                strokeColor: "white",
                strokeWeight: 1,
            },
        });

        // Create an info window
        const infoWindow = new google.maps.InfoWindow({ maxWidth: 320 });

        marker.addListener("click", () => {
            $(".chart-container").css("visibility", "visible");
            const stationInfo = `
                    <p><strong>Station no. :</strong>${station.number}</p>
                    <p><strong>Station name:</strong> ${station.name}</p>
                    <p><strong>Status:</strong> ${station.status}</p>
                    <p><strong>Available bikes:</strong> ${
                        station.available_bikes
                    }</p>
                    <p><strong>Available stands:</strong> ${
                        station.available_bike_stands
                    }</p>
                    <p><strong>Credit cards accepted:</strong> ${
                        station.banking === "True" ? "Yes" : "No"
                    }</p>
                    `;
            infoWindow.setContent(stationInfo);
            infoWindow.open(map, marker);
            drawHourlyChart(station.number,"hourly-chart");
            drawDailyChart(station.number,"daily-chart");
            drawPredictionChart(station.number,"prediction-chart")

            let stationName = `<p><strong>${station.name}</strong></p>`;
            const stationNameDiv = document.getElementById("clicked-name");
            stationNameDiv.innerHTML = stationName;
        });
    });
}

function locationErrorHandling(hasGeolocation, geolocation, position){
    geolocation.setPosition(position);
    geolocation.setContent(
        hasGeolocation? "Error: Geolocation failed.":"Error: Oops...Your browser does not support geolocation."
    );
    geolocation.open(map);
}

function displayCurrentWeather(){
    fetch("/weather").then((response) => {
        console.log(response);
        return response.json();
    }).then((data) => {
        const currentTemp = `
            <img style="display: inline-block; width: 40%" src = "${iconGenerator(data["weather"][0]["icon"])}">
            <div class="icon-day" style="display: inline-block; margin: 0; color: #333;">Now</div>
            <p style="display: inline-block; margin-right: 10px; margin: 0; color: #333;">${Math.round(data["temp"] - 273.15)}°C</p>
            `;
        const currentTempDiv = document.getElementById("current-weather");
        currentTempDiv.innerHTML = currentTemp;
      }).catch((error) => console.error(error));
}

function displayForeWeather(){
    fetch("/forecast/daily").then((response) => {
        console.log(response);
        return response.json();
    }).then((data) => {
        let foreWeather = `<div id="weather-forecast">Weather Forcast</div>`;
        var i = 0;
        weekday = ["Sunday", "Monday", "Tueday", "Wednesday", "Thursday", "Friday", "Saturday"];
        for (foreData of data) {
            if (i == 7) {
                break;
            }
            var date = new Date(foreData.dt * 1000);
            day = weekday[date.getDay()];
            if (i == 0) {
                day = "Today";
            }
            foreWeather += `
                <div class="icon-column">
                <img style="display: inline-block; width:20%" src="${iconGenerator(foreData["weather"][0]["icon"])}">
                <div class="icon-day" style="display: inline-block;">${day}</div>
                <div class="icon-temp" style="display: inline-block;">${Math.round(
                foreData["temp"]["day"] - 273.15
                )}°C</div>
                </div>
                `;
            i++;
        }
        const foreWeatherDiv = document.getElementById("fore-weather");
        foreWeatherDiv.innerHTML = foreWeather;
      }).catch((error) => console.error(error));
}

function iconGenerator(id){
    return "http://openweathermap.org/img/wn/" + id + "@2x.png";
}

google.maps.event.addDomListener(window, "load", initMap);