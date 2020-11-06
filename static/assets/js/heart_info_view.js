var dom = document.getElementById("heart");
var myChart = echarts.init(dom);
var app = {};

option = null;

function getData() {
    now = new Date(+now + oneDay);

    $.get("/heart_info_send", function (data) {
        value = data.d
    });

    return {
        name: now.toString(),
        value: [
            [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
            Math.round(value)
        ]
    };
}

var data = [];
var now = +new Date(1997, 9, 3);
var oneDay = 24 * 3600 * 1000;
var value = 0
for (var i = 0; i < 100; i++) {

    data.push(getData());
}

option = {
    title: {
        text: '心电数据'
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + ' : ' + params.value[1];
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {
        type: 'time',
        splitLine: {
            show: true
        }
    },
    yAxis: {
        type: 'value',
        splitLine: {
            show: true
        }
    },
    series: [{
        name: '模拟数据',
        type: 'line',
        showSymbol: false,
        hoverAnimation: true,
        data: data
    }]
};

setInterval(function () {

    for (var i = 0; i < 1; i++) {
        data.shift();
        data.push(getData());
    }

    myChart.setOption({
        series: [{
            data: data
        }]
    });
}, 1000);
;
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}