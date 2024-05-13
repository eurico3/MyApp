$(document).ready(function () {
    const ctx = document.getElementById("myChart").getContext("2d");

    const myChart = new Chart(ctx, {
        //type: "line",
        type:'scatter',
        data: {
            labels: [],
            datasets: [
                {
                    label: "CoinBase",
                    data: [],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3,
                    fill: false
                },
                {
                    label: "Bitcoin",
                    data: [],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'category'
                   
                },
                y: {
                    type: 'linear',
                    //position: 'bottom',
                    position: 'top',
                    ticks: {
                        stepSize: 0.1,  // Set the step size between each tick on the y-axis
                        beginAtZero: true
                    },
                },

            
            }

        }
    });

    function addData(label, priceData, quantityData) {
        myChart.data.labels.push(label);
        myChart.data.datasets[0].data.push(priceData); // Add data to the Price dataset
        myChart.data.datasets[1].data.push(quantityData); // Add data to the Quantity dataset
        myChart.update();

        document.getElementById("demo").innerHTML = priceData;

    }

    function removeFirstData() {
        myChart.data.labels.splice(0, 1);
        myChart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
    }

    const MAX_DATA_COUNT = 100;

    // Connect to the socket server.
    var socket = io.connect();

    // Receive details from server
    socket.on("updateSensorData", function (msg) {
        console.log("Received sensorData :: " + msg.date + " :: " + msg.value + ", " + msg.value2);

        // Show only MAX_DATA_COUNT data
        if (myChart.data.labels.length > MAX_DATA_COUNT) {
            removeFirstData();
        }
        
        // Add data for both Price and Quantity
        addData(msg.date, msg.value, msg.value2);
    });
});