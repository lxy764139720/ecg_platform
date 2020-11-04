from gevent import monkey
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
        return 'POST SUCCESS'
    msg = request.args.get('msg') or None
    signature = request.args.get('signature') or None
    nonce = request.args.get('nonce') or None
    if not all([msg, signature, nonce]):
        return 'invalid parameter'
    return msg


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
