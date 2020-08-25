import flask
from dht.read import Read

from dht.recording_thread import RecordingThread

import threading
app = flask.Flask(__name__)
def server():

    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return flask.jsonify({"msg": "pi-temp API"})

    @app.route('/read', methods=['GET'])
    def read():
        reader = Read()
        readings = reader.getTemp()
        return flask.jsonify({"temp": readings[0], "humidity": readings[1]})

    app.run(host="0.0.0.0", port=5000, debug=True)

def main():
    thread = RecordingThread(1, "recorder", "office")
    thread.start()
    server()

main()