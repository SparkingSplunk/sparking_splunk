
window.chartColors = {
    red: "#fc050520",
    orange: "#ff9d0020",
    yellow: "#e7fc0520",
    blue: "#00a2ff20",

    green: "#2efc0520",
    grey: "#7a787a20",

    purple: "#dd00ff20",
    teal: "#00ffee20",
    black: "#000000"

}
const presets = window.chartColors;
function randomScalingFactor() {
    return Math.round((Math.random()*2-1)*100);
}
var config = {
    type: 'line',
    data: {
        datasets: [{
            label: 'metric_value',
            backgroundColor: window.chartColors.black,
            borderColor: window.chartColors.black,
            data: [],
            fill: false,
        }, {
            label: '0',
            backgroundColor: presets.red,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '1',
            backgroundColor: presets.red,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '2',
            backgroundColor: presets.orange,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '3',
            backgroundColor: presets.orange,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '4',
            backgroundColor: presets.yellow,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '5',
            backgroundColor: presets.yellow,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '6',
            backgroundColor: presets.blue,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '7',
            backgroundColor: presets.blue,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '8',
            backgroundColor: presets.yellow,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '9',
            backgroundColor: presets.yellow,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '10',
            backgroundColor: presets.orange,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '11',
            backgroundColor: presets.orange,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '12',
            backgroundColor: presets.red,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }, {
            label: '13',
            backgroundColor: presets.red,
            borderWidth: 0,
            pointRadius: 0,
            data: [],
            fill: '+1'
        }]
    },
    options: {
        responsive: true,
        title: {
            display: false,
            text: 'Chart.js Line Chart'
        },
        legend: {
            display: false,
        },
        tooltips: {
            enabled: false,
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
                    labelString: 'Time(s)'
                }
            }],
            yAxes: [{
                display: true,
                stacked: false,
                scaleLabel: {
                    display: true,
                    labelString: 'Clicks'
                }
            }]
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
}



var colorNames = Object.keys(window.chartColors);

const next_points = [];


const time_set = new Set()
function addDataPoint(time, value, l0, l1, l2, l3, u0, u1, u2, u3) {
    if (config.data.datasets.length > 0) {
        if (time_set.has(String(time) + String(value))) return;
        time_set.add(String(time) + String(value));

        next_points.push({
            time: (new Date(time)).toISOString().slice(-13, -5),
            value: value,
            l0:l0,
            l1:l1,
            l2:l2,
            l3:l3,
            u0:u0,
            u1:u1,
            u2:u2,
            u3:u3,
        })
    } 
}

let add_point_delay = 100;
let addinng_points = false;

function addPoints() {

    add_point_delay = Math.max(add_point_delay - (((next_points.length-3)/5)*Math.abs((next_points.length-3)/5))*40, 0);

    if (next_points.length > 0) {
        const point = next_points.shift();
        if (config.data.datasets[0].data.length > 200) pop();
        config.data.labels.push(point.time);

        config.data.datasets[0].data.push(point.value);
        config.data.datasets[1].data.push(point.u3);
        config.data.datasets[2].data.push(point.u2);
        config.data.datasets[3].data.push(point.u2);
        config.data.datasets[4].data.push(point.u1);
        config.data.datasets[5].data.push(point.u1);
        config.data.datasets[6].data.push(point.u0);
        config.data.datasets[7].data.push(point.u0);
        config.data.datasets[8].data.push(point.l0);
        config.data.datasets[9].data.push(point.l0);
        config.data.datasets[10].data.push(point.l1);
        config.data.datasets[11].data.push(point.l1);
        config.data.datasets[12].data.push(point.l2);
        config.data.datasets[13].data.push(point.l2);
        config.data.datasets[14].data.push(point.l3);

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