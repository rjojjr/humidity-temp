import mysql.connector
import datetime

import uuid

#Debug SQL
from api.models.summary import Summary

from api.models.records import ReadingRecord

SQL_DEBUG = 1

class MySql:

    def executeStatement(self, statement):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
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
                    host="localhost",
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

    def executeStatementRemote(self, statement, host):
        try:
            mydb = mysql.connector.connect(
                host=host,
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

    def latestReading(self, room):
        statement = "SELECT temp, humidity FROM readings WHERE time = (SELECT MAX(time) FROM readings  WHERE room  = '" + room + "');"
        result = self.executeStatementReturn(statement)
        for i in result:
            return [str(i[0]), str(i[1])]

    def latestReadingWithTime(self, room):
            statement = "SELECT temp, humidity, time FROM readings WHERE time = (SELECT MAX(time) FROM readings  WHERE room  = '" + room + "');"
            result = self.executeStatementReturn(statement)
            for i in result:
                return [str(i[0]), str(i[1]), str(i[2])]

    def getRooms(self):
        statement = "SELECT DISTINCT room FROM readings"
        result = self.executeStatementReturn(statement)
        rooms = []
        for i in result:
            rooms.append(i[0])
        return rooms

    def insertRecord(self, temp, humidity, room):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        statement = "INSERT INTO readings (`room`, `temp`, `humidity`, `time`) VALUES ('" + room + "','" + temp + "','" + humidity + "','"  + formatted_date + "');"
        self.executeStatement(statement)

    def insertRecordWithTs(self, temp, humidity, room, time_stamp):
        statement = "INSERT INTO readings (`room`, `temp`, `humidity`, `time`) VALUES ('" + room + "','" + temp + "','" + humidity + "','"  + time_stamp + "');"
        self.executeStatement(statement)

    def transferRecords(self, host):
        statement = "SELECT temp, humidity, time, room, id FROM readings;"
        result = self.executeStatementRemote(statement, host)
        records = []
        for i in result:
            print("transferring record " + i[4] + " from old host")
            self.insertRecordWithTs(i[0], i[1], i[3], i[2])
        return len(records)

    def avgTemp(self, room):
        statement = "SELECT AVG(temp) 'Average Temp' FROM readings WHERE room = '" + room + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def avgTempToday(self, room):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT AVG(temp) 'Average Temp' FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + now.strftime('%Y-%m-%d') + "' AND '" + tom.strftime('%Y-%m-%d') + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def avgHumidityToday(self, room):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT AVG(humidity) 'Average Temp' FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + now.strftime('%Y-%m-%d') + "' AND '" + tom.strftime('%Y-%m-%d') + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def submitSmsNotification(self, recipients, message, subject):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        statement = "INSERT INTO notifications (`uuid`, `type`, `sent`, `subject`, `message`, `recipients`, `generated_time`, `sent_time`) VALUES ('" + uuid.uuid1() + "','sms','f','"  + subject + "','"  + message + "','"  + recipients + "','"  + formatted_date + "','"  + formatted_date + "');"
        self.executeStatement(statement)

    def getUnsentSmsNotifications(self, room, start, stop):
        now = datetime.datetime.today()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        statement = "SELECT `id`, `uuid`, `type`, `sent`, `subject`, `message`, `recipients`, `generated_time` FROM notifications WHERE sent = 'f';"
        result = self.executeStatementReturn(statement)
        notifications = []
        for i in result:
            notifications.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
            statement = "UPDATE notifications SET sent = 't', sent_time =  '" + formatted_date + "' WHERE id = '" + i[0] + "';"
            self.executeStatement(statement)
        return notifications

    def avgHumidity(self, room):
        statement = "SELECT AVG(humidity) 'Average Humidity' FROM readings WHERE room = '" + room + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def avgTempBetween(self, room, start, stop):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT AVG(temp) 'Average Temp' FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + start + "' AND '" + stop + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def tempDiffBetween(self, room, start, stop):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT MAX(temp), MIN(temp) 'Average Temp' FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + start + "' AND '" + stop + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return [i[0], i[1]]

    def getRecordsBetween(self, room, start, stop):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT temp, humidity, time FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + start + "' AND '" + stop + "';"
        result = self.executeStatementReturn(statement)
        records = []
        for i in result:
            records.append(ReadingRecord(room, i[0], i[1], i[2]))
        return records

    def getRecordsBetween(self, start, stop):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT temp, humidity, time, room FROM readings WHERE time BETWEEN '" + start + "' AND '" + stop + "';"
        result = self.executeStatementReturn(statement)
        records = []
        for i in result:
            records.append(ReadingRecord(i[3], i[0], i[1], i[2]))
        return records

    def avgHumidityBetween(self, room, start, stop):
        now = datetime.datetime.today()
        tom = now + datetime.timedelta(days = 1)
        statement = "SELECT AVG(humidity) 'Average Temp' FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + start + "' AND '" + stop + "';"
        result = self.executeStatementReturn(statement)
        for i in result:
            return i[0]

    def getAllReadings(self):
        statement = "SELECT * FROM readings;"
        result = self.executeStatementReturn(statement)
        for i in result:
            print("id: " + str(i[0]) + " room: " + i[1] + " temp: " + str(i[2]) + " humidity: " + str(i[3]) + " time: " + str(i[4]))

    def getAllReadings(self, room, startDate, endDate):
        statement = "SELECT * FROM readings WHERE room = '" + room + "' AND time BETWEEN '" + startDate + "' AND '" + endDate + "';"
        result = self.executeStatementReturn(statement)
        r = []
        for i in result:
            r.append(i)
        return r

    def runQuery(self, statement):
        result = self.executeStatementReturn(statement)
        for i in result:
            row = ""
            for k in i:
                row = row + " " + str(k)
            print(row)
