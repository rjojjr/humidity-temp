import tm1637
import Adafruit_DHT
import mysql.connector
import datetime
from MySql import MySql

import sys

tm = tm1637.TM1637(clk=23, dio=24)

# v1.0.00a
import time

# DHT Pin
DHT_PIN = 4
# Print each reading
DEBUG = 1
temp = 0
humidity = 0
temperature = 0

room = "office"

if len(sys.argv) == 2:
    room = sys.argv[1]

def getTemp():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    temp = int((1.8 * temperature) + 32)
    humidity = int(humidity)
    t = str(int(temp))
    h = str(int(humidity))
    if (len(t) == 1):
        t = "0" + t[0]
    if (len(h) == 1):
        h = "0" + h[0]
    tm.numbers(int(t[0] + t[1]), int(h[0] + h[1]))
    if (DEBUG == 1):
        print("Temp: " + str(temp) + " Humidity: " + str(humidity))
    con = MySql()
    con.insertRecord(t, h, room)

while True:
    treadings = [0]
    hreadings = [0]
    print("Reading...")
    getTemp()
    time.sleep(15)