import tm1637
import Adafruit_DHT
import mysql.connector
import datetime

tm = tm1637.TM1637(clk=23, dio=24)

# v1.0.00a
import time

# DHT Pin
DHT_PIN = 4
# Print each reading
DEBUG = 1
#Debug SQL
SQL_DEBUG = 1
temp = 0
humidity = 0
temperature = 0

def execute(statement):
    try:
        mydb = mysql.connector.connect(
            host="192.168.1.12",
            port="3306",
            user="pythonuser",
            password="UEAkJFcwcmRQQCQkVzByZAo=",
            database="py_temp"
        )

        mycursor = mydb.cursor()
        if (SQL_DEBUG == 1):
            print("Executing SQL statement: " + statement)
        mycursor.execute(statement)
        if (SQL_DEBUG == 1):
            print("Committing row to db")
        mydb.commit()
    except:
        print("An SQL error has happened")

def insertRecord(temp, humidity):
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    statement = "INSERT INTO readings (`room`, `temp`, `humidity`, `time`) VALUES ('office','" + temp + "','" + humidity + "','"  + formatted_date + "');"
    execute(statement)

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
    insertRecord(t, h)

while True:
    treadings = [0]
    hreadings = [0]
    print("Reading...")
    getTemp()
    time.sleep(15)