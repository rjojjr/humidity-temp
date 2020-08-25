from api.dht.MySql import MySql

sql = MySql()

def executeCustomSql(sql):
    userInput = input("Enter SQl Statement: ")
    sql.runQuery(userInput)

def avg(type):
    userInput = input("Enter room/sensor name: ")
    room = str(userInput)
    userInput = input("Enter 0 to input date range: ")
    if userInput == 0:
        avgBetween(type, room)
    else:
        if type == "temp" :
            print("Avg. Temp = " + str(sql.avgTemp(room)))
        else:
            print("Avg. Humidity = " + str(sql.avgHumidity(room)))


def avgBetween(type, room):
    userInput = input("Enter starting date: ")
    start = str(userInput)
    userInput = input("Enter ending date: ")
    stop = str(userInput)
    if type == "temp" :
        print("Avg. Temp = " + str(sql.avgTempBetween(room, start, stop)))
    else:
        print("Avg. Humidity = " + str(sql.avgHumidityBetween(room, start, stop)))

userInput = -1

while userInput != 0:
    print("1. Avg Temp")
    print("2. Avg Humidity")
    print("3. Print all Rows")
    print("4. Execute Statement")
    print("0. Exit")
    userInput = input("Enter your selection: ")
    if userInput == 1:
        avg("temp")
    elif userInput == 2:
        avg("hum")
    elif userInput == 3:
        sql.getAllReadings()
    elif userInput == 4:
        executeCustomSql(sql)
    elif userInput != 0:
        print("Invalid input")