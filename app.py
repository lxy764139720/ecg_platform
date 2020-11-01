from flask import Flask, request, render_template
from models import User
from flask_login import LoginManager

app = Flask(__name__)  # 创建 Flask 应用


# app.secret_key = 'abc'  # 设置表单交互密钥
# login_manager = LoginManager()  # 实例化登录管理对象
# login_manager.init_app(app)  # 初始化应用
# login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint


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
