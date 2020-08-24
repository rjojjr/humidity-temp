import mysql.connector
import datetime

#Debug SQL
SQL_DEBUG = 1

class MySql:

    def execute(self, statement):
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

    def insertRecord(self, temp, humidity):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        statement = "INSERT INTO readings (`room`, `temp`, `humidity`, `time`) VALUES ('office','" + temp + "','" + humidity + "','"  + formatted_date + "');"
        self.execute(statement)