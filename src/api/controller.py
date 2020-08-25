import flask
from dht.read import Read

from flask import request

from dht.recording_thread import RecordingThread

import threading

thread = None
app = flask.Flask(__name__)
def server():

    app.config["DEBUG"] = True
    def shutdown_server():
        thread.stop()
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
       shutdown_server()
       return 'Server shutting down...'

    @app.route('/', methods=['GET'])
    def home():
        return flask.jsonify({"msg": "pi-temp API"})

    @app.route('/read', methods=['GET'])
    def read():
        reader = Read()
        readings = reader.getTemp()
        return flask.jsonify({"temp": readings[0], "humidity": readings[1]})

    app.run(host="0.0.0.0", port=5000, debug=True)

def main(room):
    thread = RecordingThread(1, "recorder", room)
    thread.start()
    server()

