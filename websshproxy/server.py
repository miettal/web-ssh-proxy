# coding=utf-8
from . import app
from . import socketio

if __name__ == '__main__':
    socketio.run(app)
