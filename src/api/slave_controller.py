import flask
from dht.read import Read

from flask import request

from flask_cors import CORS

from dht.MySql import MySql
from summary_service import SummaryService

from dht.recording_thread import RecordingThread

import threading

app = flask.Flask(__name__)
cors = CORS(app)
def server(thread):

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
        return flask.jsonify({"msg": "py-temp Slave API"})

    @app.route('/read', methods=['GET'])
    def read():
        reader = Read()
        readings = reader.getTemp()
        return flask.jsonify({"temp": readings[0], "humidity": readings[1]})

    @app.route('/summary/<room>', methods=['GET'])
    def summary(room):
        assert room == request.view_args['room']
        summary = SummaryService()
        return flask.jsonify(summary.getSlaveSummary(room))

    app.run(host="0.0.0.0", port=5000, debug=True)

def main(room):
    thread = RecordingThread(1, "recorder", room)
    thread.start()
    server(thread)

