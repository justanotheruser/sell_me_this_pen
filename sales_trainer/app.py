import logging

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from sales_trainer.trainer_store import trainer_store

app = Flask(__name__)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    logger.debug(f'Client {request.sid} connected')  # type: ignore
    trainer_store.add(request.sid)
    emit('message', "Продайте мне эту ручку")


@socketio.on('disconnect')
def handle_disconnect(reason):
    logger.debug(f'Client {request.sid} disconnected: {reason}')  # type: ignore
    trainer_store.remove(request.sid)


@socketio.on('message')
def handle_message(data):
    logger.info(f'Received message from {request.sid}')
    trainer = trainer_store.get(request.sid)
    if not trainer:
        return
    response = trainer.invoke(data)
    emit('message', response)


if __name__ == '__main__':
    # socketio.run(app, host='localhost', port=8080, debug=True)
    socketio.run(app, host='localhost', port=8080)
