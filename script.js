// 初始化地图
let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3498, lng: -6.2603 },
    zoom: 14,
  });

  // 获取所有站点数据
  fetch("/api/stations")
    .then(response => response.json())
    .then(stations => {
      // 将站点信息加入到地图中
      stations.forEach(station => {
        const location = { lat: station.latitude, lng: station.longitude };
        const marker = new google.maps.Marker({
          position: location,
          map: map,
          title: station.name,
          icon: getMarkerIcon(station.available_bikes, station.bike_stands),
        });

        // 点击站点时显示站点信息
        marker.addListener("click", () => {
          showStationInfo(station);
        });
      });
    })
    .catch(error => console.error(error));

  // 获取天气数据并显示
  fetch("/api/weather")
    .then(response => response.json())
    .then(weatherData => {
      if (weatherData.length > 0) {
        const weather = weatherData[0];
        const temp = Math.round(weather.temperature);
        const iconClass = `wi-owm-${weather.icon}`;

        $("#temp").text(`${temp}°C`);
        $("#weather-icon").addClass(iconClass);
      }
    })
    .catch(error => console.error(error));
}

// 根据可用车位数量获取标记图标
function getMarkerIcon(availableBikes, totalStands) {
  const availability = availableBikes / totalStands;
  const availabilityLevel = Math.min(Math.floor(availability / 0.1), 8);
  return {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: "#fff",
    fillOpacity: 1,
    strokeColor: "#000",
    strokeOpacity: 1,
    strokeWeight: 2,
    scale: 5 + availabilityLevel * 3,
  };
}

// 显示站点信息
function showStationInfo(station) {
  $("#station-name").text(station.name);
  $("#station-address").text(station.address);
  $("#station-availability").text(`Available Bikes: ${station.available_bikes}, Total Bike Stands: ${station.bike_stands}`);

  // 获取并显示小时级可用率数据
  fetch(`/api/hourly_occupancy?station_id=${station.number}`)
    .then(response => response.json())
    .then(occupancy => {
      const chartData = occupancy.map(data => [moment(data.time).valueOf(), data.occupancy_rate * 100]).sort((a, b) => a[0] - b[0]);
      drawChart(chartData);
    })
    .catch(error => console.error(error));
}

// 绘制站点小时级可用率图表
function drawChart(chartData) {
  Highcharts.chart("chart", {
    chart: {
      type: "line",
    },
    title: {
      text: "Hourly Occupancy",
    },
    xAxis: {
      type: "datetime",
      title: {
        text: "Time",
      },
    },
    yAxis: {
      title: {
        text: "Occupancy Rate (%)",
      },
    },
    series: [
      {
        name: "Occupancy Rate",
        data: chartData,
      },
    ],
  });
}

// 监听搜索表单提交事件
$("form").submit(event => {
    event.preventDefault();
    const startLocation = $("#start-location").val();
    const endLocation = $("#end-location").val();
    
    // 根据起始点和终点进行路线规划
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    
    const request = {
        origin: startLocation,
        destination: endLocation,
        travelMode: google.maps.TravelMode.BICYCLING
    };
    
    // 发送路线规划请求
    directionsService.route(request, (result, status) => {
        if (status == google.maps.DirectionsStatus.OK) {
            // 显示路线
            directionsRenderer.setDirections(result);
            // 显示路线总长度和时间
            const distance = result.routes[0].legs[0].distance.text;
            const duration = result.routes[0].legs[0].duration.text;
            alert(`Distance: ${distance}, Duration: ${duration}`);
        } else {
            alert("Directions request failed due to " + status);
        }
    });
});
