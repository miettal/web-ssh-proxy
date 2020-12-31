# coding=utf-8
from flask import Flask
from flask import render_template

from flask_socketio import SocketIO

# flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
