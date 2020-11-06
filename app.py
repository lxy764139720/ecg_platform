import json
# from gevent import monkey
from flask import Flask, request, render_template
from flask_sse import sse

# monkey.patch_all()
app = Flask(__name__)  # 创建 Flask 应用
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")


@app.route('/')
def hello_sse():
    return render_template("helloSSE.html")


@app.route('/hello')
def publish():
    sse.publish({"message": "Hello!"}, type="greeting")
    sse.publish({"beat": 1}, type="beat")
    return "Message Sent!"


@app.route('/ecg/login', methods=['GET', 'POST'])
def login():
    return render_template('login_register.html')


@app.route('/ecg/register', methods=['GET', 'POST'])
def register():
    return render_template('index.html')


@app.route('/ecg/index')
def index():
    return render_template('index.html')


@app.route('/ecg/chart')
def chart():
    return render_template('chart.html')


@app.route('/ecg/httptest', methods=['GET', 'POST'])
def httptest():
    if request.method == 'POST':
        print('**** Receive Post Data *****')
        print(request.data)

        onenet_data = json.loads(request.data)
        msg = onenet_data['msg']
        msg_time = msg['at']  # timestrap
        msg_type = msg['type']  # 1:data 2:online/offline
        msg_devid = msg['dev_id']  # device id

        if msg_type == 2:
            # online/offline message
            if msg['status'] == 1:
                sse.publish({"device_on": "online"}, type="device")
                sse.publish({"device_id": msg_devid}, type="device")
            if msg['status'] == 0:
                sse.publish({"device_off": "offline"}, type="device")
        if msg_type == 1:
            # data message
            msg_value = msg['value']  # heart beat data
            sse.publish({"beat": msg_value}, type="data")
            sse.publish({"time": msg_time}, type="data")
            print('sent')

        return 'POST SUCCESS'
    msg = request.args.get('msg') or None
    signature = request.args.get('signature') or None
    nonce = request.args.get('nonce') or None
    if not all([msg, signature, nonce]):
        return 'invalid parameter'
    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
