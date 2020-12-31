# coding=utf-8
import collections

from flask import Flask
from flask import request
from flask import render_template

from flask_socketio import SocketIO

from flask_executor import Executor

import paramiko


# flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio
socketio = SocketIO(app)
# executor
executor = Executor()
executor.init_app(app)


input_buf = collections.defaultdict(str)


def start_session(sid, hostname, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password, timeout=1)
        channel = ssh.invoke_shell()
        socketio.emit('ssh-status', 'connected', json=True, to=sid)
        while True:
            if input_buf[sid]:
                channel.send(input_buf[sid].encode('utf-8'))
                input_buf[sid] = ''
            if channel.recv_ready():
                ssh_output = channel.recv(65536).decode('utf-8')
                socketio.emit('ssh-output', ssh_output, to=sid)
            socketio.sleep(0.1)
    except Exception as e:
        socketio.emit('ssh-status', str(e), json=True, to=sid)


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on('ssh-connect')
def handle_ssh_connect(json):
    try:
        print("{:s}@{:s}".format(json['username'], json['hostname']))
        executor.submit(start_session, request.sid, json['hostname'], json['port'], json['username'], json['password'])
    except Exception as e:
        socketio.emit('ssh-status', str(e), json=True, to=request.sid)


@socketio.on('ssh-input')
def handle_ssh_input(json):
    input_buf[request.sid] += json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
