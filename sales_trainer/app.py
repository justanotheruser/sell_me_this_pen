import logging

from apscheduler import Scheduler
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from sales_trainer.config import config
from sales_trainer.trainer.trainer_store import trainer_store_factory

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=config.hosting.cors.allow_origins)
scheduler = Scheduler()
scheduler.start_in_background()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html', domain=config.hosting.domain, port=config.hosting.port)


@socketio.on('connect')
def handle_connect():
    logger.debug(f'Client {request.sid} connected')  # type: ignore
    trainer_store = trainer_store_factory(config=config.trainer, scheduler=scheduler)
    trainer_store.add(request.sid)
    emit('message', "Продайте мне эту ручку")


@socketio.on('disconnect')
def handle_disconnect(reason):
    logger.debug(f'Client {request.sid} disconnected: {reason}')  # type: ignore
    trainer_store = trainer_store_factory(config=config.trainer, scheduler=scheduler)
    trainer_store.remove(request.sid)


@socketio.on('message')
def handle_message(data):
    logger.info(f'Received message from {request.sid}')
    trainer_store = trainer_store_factory(config=config.trainer, scheduler=scheduler)
    trainer = trainer_store.get(request.sid)
    if not trainer:
        return
    response = trainer.invoke(data)
    emit('message', response)


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080)
