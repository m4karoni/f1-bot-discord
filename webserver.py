from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def here():
  return 'I\'m alive!'


def run():
  app.run(host='0.0.0.0', port=8181)


def keep_alive():
  t = Thread(target=run)
  t.start()
