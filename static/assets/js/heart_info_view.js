// 打开到流终点的 SSE 连接
var source = new EventSource("{{ url_for('sse.stream') }}")
var dom = document.getElementById("heart");
var myChart = echarts.init(dom);
var app = {};
option = null;
var data = [];

// 可选回调, 建立连接时调用
source.onopen = function () {
    console.log("开始发送");
};

// 可选回调, 连接失败时调用
source.onerror = function () {
    console.log("连接错误");
}

// 监听 "greeting" 事件, 调用自定义代码
source.addEventListener('greeting', function (event) {
    var data = JSON.parse(event.data);
    console.log("The server says: " + data.message);
}, false);

// 监听 "beat" 事件, 调用自定义代码
source.addEventListener('beat', function (event) {
    var id = JSON.parse(event.id);
    var data = JSON.parse(event.data);
    console.log(id + " : " + data);
    if (id === "beat") {
        data.shift();
        data.push(data.message);
        myChart.setOption({
            series: [{data: data}]
        });
    }
}, false);

// 监听 "device" 事件, 调用自定义代码
source.addEventListener('device', function (event) {
    var id = JSON.parse(event.id);
    var data = JSON.parse(event.data);
    console.log(id + " : " + data);
}, false);

// 监听 "error" 事件, 调用自定义代码
source.addEventListener("error", function (event) {
    console.log("Failed to connect to event stream.")
}, false);

// 监听所有事件, 不明确指定事件类型.
source.onmessage = function (event) {
    console.log(event.id, event.data);
    // 如果 服务器发送 "CLOSE" 消息 ID, 关闭 SSE 连接.
    if (event.id === "CLOSE") {
        source.close();
    }
}

option = {
    title: {
        text: '动态数据 + 时间坐标轴'
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            return params.name;
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

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}