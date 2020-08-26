#!/usr/bin/env bash
# Run with sudo in root project directory
apt-get install python-dev python-pip
pip install wiringpi2
pip install Adafruit_DHT
pip install flask
python -m pip install mysql-connector-python
pip install -U flask-cors