import mysql.connector
import datetime

#Debug SQL
SQL_DEBUG = 1

class MySql:

    def executeStatement(self, statement):
        try:
            mydb = mysql.connector.connect(
                host="192.168.1.169",
                port="3306",
                user="pythonuser",
                password="UEAkJFcwcmRQQCQkVzByZAo=",
                database="py_temp"
            )

            mycursor = mydb.cursor(buffered=True)
            if (SQL_DEBUG == 1):
                print("Executing SQL statement: " + statement)
            mycursor.execute(statement)
            if (SQL_DEBUG == 1):
                print("Committing to db")
            mydb.commit()
        except:
            print("An SQL error happened")

    def executeStatementReturn(self, statement):
            try:
                mydb = mysql.connector.connect(
                    host="192.168.1.169",
                    port="3306",
                    user="pythonuser",
                    password="UEAkJFcwcmRQQCQkVzByZAo=",
                    database="py_temp"
                )

                mycursor = mydb.cursor(buffered=True)
                if (SQL_DEBUG == 1):
                    print("Executing SQL statement: " + statement)
                mycursor.execute(statement)
                if (SQL_DEBUG == 1):
                    print("Committing to db")
                mydb.commit()
                records = mycursor.fetchall()
                return records
            except:
                print("An SQL error happened")
                return ""

    def insertRecord(self, temp, humidity, room):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        statement = "INSERT INTO readings (`room`, `temp`, `humidity`, `time`) VALUES ('" + room + "','" + temp + "','" + humidity + "','"  + formatted_date + "');"
        self.executeStatement(statement)

    def avgTemp(self):
        statement = "SELECT AVG(temp) 'Average Temp' FROM readings;"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def avgHumidity(self):
        statement = "SELECT AVG(humidity) 'Average Humidity' FROM readings;"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def getAllReadings(self):
        statement = "SELECT * FROM readings;"
        result = self.executeStatementReturn(statement)
        for i in result:
            print("id: " + str(i[0]) + " room: " + i[1] + " temp: " + str(i[2]) + " humidity: " + str(i[3]) + " time: " + str(i[4]))

    def runQuery(self, statement):
        result = self.executeStatementReturn(statement)
        for i in result:
            row = ""
            for k in i:
                row = row + " " + str(k)
            print(row)