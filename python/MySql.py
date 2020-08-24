import mysql.connector
import datetime

def execute(statement):
    mydb = mysql.connector.connect(
        host="localhost",
        user="pythonuser",
        password="UEAkJFcwcmRQQCQkVzByZAo=",
        database="py_temp"
    )

    mycursor = mydb.cursor()
    mycursor.execute(statement)

def insertRecord(temp, humidity):
    now = datetime.datetime.utcnow()
    statement = "INSERT INTO readings (temp, humidity, time) VALUES(temp, humidity, now." + strftime('%Y-%m-%d %H:%M:%S') + ")"
    execute(statement)