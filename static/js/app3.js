$(document).ready(function () {
    const ctx = document.getElementById("myChart").getContext("2d");
  
    const myChart = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [{ label: "Price",  }, { label: "Price2",  }],
      },
      options: {
        borderWidth: 3,
        borderColor: ['rgba(255, 99, 132, 1)',],
      },
    });
  
    function addData(label, data) {
      myChart.data.labels.push(label);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
      myChart.update();
    }
  
    function removeFirstData() {
      myChart.data.labels.splice(0, 1);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
      });
    }
  
    const MAX_DATA_COUNT = 100;
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
    var socket = io.connect();
  
    //receive details from server
    socket.on("updateSensorData", function (msg) {
      console.log("Received sensorData :: " + msg.date + " :: " + msg.value);
    
  
      // Show only MAX_DATA_COUNT data
      if (myChart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });

    socket.on("updateSensorData2", function (msg) {
      console.log("Received sensorData2 :: " + msg.date + " :: " + msg.value);
    
  
     //  Show only MAX_DATA_COUNT data
      if (myChart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });



  });