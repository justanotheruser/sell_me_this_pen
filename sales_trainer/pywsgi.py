from gevent import monkey

# https://iximiuz.com/en/posts/flask-gevent-tutorial/
monkey.patch_all()


from sales_trainer.app import app, socketio  # noqa[E402]

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080)
