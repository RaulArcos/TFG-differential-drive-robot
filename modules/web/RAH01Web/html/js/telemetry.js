var ctx = document.getElementById('velocityChart').getContext('2d');
var velocityChart = new Chart(ctx, {
    type: 'line', // Line chart type
    data: {
        labels: [], // Time labels
        datasets: [{
            label: 'Linear Speed',
            backgroundColor: 'rgb(255, 154, 0)',
            borderColor: 'rgb(255, 154, 0)',
            data: [],
            fill: false,
        }, {
            label: 'Angular Speed',
            backgroundColor: 'rgb(54, 162, 235)',
            borderColor: 'rgb(54, 162, 235)',
            data: [],
            fill: false,
        }]
    },
    options: {
        scales: {
            x: {
                type: 'realtime',
                realtime: {
                    delay: 2000, // Delay of 2 seconds
                    onRefresh: chart => {
                        // This function will be defined to add data to the chart
                    }
                }
            }
        }
    }
});