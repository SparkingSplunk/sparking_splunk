
console.log('hello david');
window.chartColors = {
    red: "#fc0505",
    blue: "#2200ff"
}
function randomScalingFactor() {
    return Math.round((Math.random()*2-1)*100);
}
var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var config = {
    type: 'line',
    data: {
        datasets: [{
            label: 'My First dataset',
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: [],
            fill: false,
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Chart.js Line Chart'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};

window.onload = function() {
    console.log('hey')
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
}

document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
        dataset.data = dataset.data.map(function() {
            return randomScalingFactor();
        });

    });

    window.myLine.update();
});

var colorNames = Object.keys(window.chartColors);
document.getElementById('addDataset').addEventListener('click', function() {
    var colorName = colorNames[config.data.datasets.length % colorNames.length];
    var newColor = window.chartColors[colorName];
    var newDataset = {
        label: 'Dataset ' + config.data.datasets.length,
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
});

document.getElementById('addData').addEventListener('click', function() {
    if (config.data.datasets.length > 0) {
        var month = MONTHS[config.data.labels.length % MONTHS.length];
        config.data.labels.push(month);

        config.data.datasets.forEach(function(dataset) {
            dataset.data.push(randomScalingFactor());
        });

        window.myLine.update();
    }
});

document.getElementById('removeDataset').addEventListener('click', function() {
    config.data.datasets.splice(0, 1);
    window.myLine.update();
});

document.getElementById('removeData').addEventListener('click', function() {
    // config.data.labels.splice(-1, 1); // remove the label first
    config.data.labels = config.data.labels.slice(1)
    config.data.datasets.forEach(function(dataset) {
        // dataset.data.pop();
        dataset.data = dataset.data.slice(1);
    });

    window.myLine.update();
});

const next_points = [];


const time_set = new Set()
function addDataPoint(time, value) {
    if (config.data.datasets.length > 0) {
        if (time_set.has(time)) return;
        time_set.add(time);

        next_points.push({
            time: (new Date(time*1000)).toISOString().slice(-13, -5),
            value: value,
        })
    } 
}

let add_point_delay = 100;
let addinng_points = false;

function addPoints() {

    add_point_delay = Math.max(add_point_delay - (((next_points.length-5)/5)*Math.abs((next_points.length-5)/5))*40, 0);
    console.log(add_point_delay);

    if (next_points.length > 0) {
        const point = next_points.shift();
        if (config.data.datasets[0].data.length > 200) pop();
        config.data.labels.push(point.time); 
        config.data.datasets.forEach(dataset => {
            dataset.data.push(point.value);
        });
        window.myLine.update();
    }
    setTimeout(() => {
        addPoints();
    }, add_point_delay);
}



function pop() {
    config.data.labels = config.data.labels.slice(1)
    config.data.datasets.forEach(function(dataset) {
        dataset.data.shift();
    });
    // window.myLine.update();
}