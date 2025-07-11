from gevent import monkey
monkey.patch_all()
from flask_socketio import SocketIO, emit


import os
from gevent.pywsgi import WSGIServer
from app import app, socketio


if __name__ == '__main__':
    # socketio.run(app, host='localhost', port=8080, debug=True)
    socketio.run(app, host='localhost', port=8080)
