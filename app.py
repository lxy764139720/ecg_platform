from flask import Flask, request

app = Flask(__name__)


@app.route('/ecg/index')
def hello_world():
    return 'Hello World!'


@app.route('/ecg/httptest')
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
    app.run(host='0.0.0.0', debug=True)
