import logging

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from sales_trainer.config import load_config

cfg = load_config()
app = Flask(__name__)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    logger.debug('Client connected')


@socketio.on('disconnect')
def handle_disconnect(reason):
    logger.debug(f'Client disconnected: {reason}')


@socketio.on('message')
def handle_message(data):
    logger.info(f'Received message from {data}')
    emit('message', f'Echo: {data}')


if __name__ == '__main__':
    # socketio.run(app, host='localhost', port=8080, debug=True)
    socketio.run(app, host='localhost', port=8080)
