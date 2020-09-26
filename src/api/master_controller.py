import flask

from flask import request

from flask_cors import CORS

from api.dht.MySql import MySql

from api.models.interval_request import IntervalRequest

from api.summary_service import SummaryService

import threading

app = flask.Flask(__name__)
cors = CORS(app)
def server():

    app.config["DEBUG"] = True
    def shutdown_server():
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
        return flask.jsonify({
        "name": "py-temp Master API"
        })

    @app.route('/esp/submit', methods=['GET'])
    def espSub():
        temp = request.args.get('temp')
        hum = request.args.get('humidity')
        room = request.args.get('room')
        sql = MySql()
        sql.insertRecord(temp, hum, room)
        return flask.jsonify({
        "msg": "okay"
        })

    @app.route('/summary/<room>', methods=['GET'])
    def summary(room):
        assert room == request.view_args['room']
        summary = SummaryService()
        return flask.jsonify(summary.getSummary(room))

    @app.route('/summary', methods=['GET'])
    def summaryAll():
        summary = SummaryService()
        return flask.jsonify(summary.getSummaries())

    @app.route('/chart', methods=['POST'])
    def chart():
        req = IntervalRequest(request.form.get('type'), request.form.get('startDate'), request.formget('endDate'))
        summary = SummaryService()
        return flask.jsonify(summary.getChart(req))

    app.run(host="0.0.0.0", port=8080, debug=True)

def main():
    server()

