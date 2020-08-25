import flask
from dht.read import Read
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify({"msg": "pi-temp API"})

@app.route('/read', methods=['GET'])
def read():
    reader = Read()
    readings = reader.dummy()
    return flask.jsonify({"temp": readings[0], "humidity": readings[1]})

app.run()