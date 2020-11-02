import time

import redis
from gevent import monkey
from flask import Flask, request, render_template, Blueprint
from flask_sse import sse
from flask_session import Session

# monkey.patch_all()
# r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
app = Flask(__name__)  # 创建 Flask 应用
app.config["REDIS_URL"] = "redis://localhost"
# app.config['SECRET_KEY'] = 'secret_key'
# app.config['REDIS_HOST'] = "127.0.0.1"  # redis数据库地址
# app.config['REDIS_PORT'] = 6379  # redis 端口号
# app.config['REDIS_DB'] = 0  # 数据库名
# app.config['REDIS_EXPIRE'] = 60  # redis 过期时间60秒
app.register_blueprint(sse, url_prefix="/stream")


# app.secret_key = 'abc'  # 设置表单交互密钥
# login_manager = LoginManager()  # 实例化登录管理对象
# login_manager.init_app(app)  # 初始化应用
# login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint


@app.route('/')
def hello_sse():
    return render_template("helloSSE.html")


@app.route('/hello')
def publish():
    i = 8
    while i > 0:
        sse.publish({"message": "Hello!"}, type="greeting")
        time.sleep(1000)
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
