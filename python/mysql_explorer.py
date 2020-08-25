from MySql import MySql

sql = MySql()
userInput = -1
while userInput != 0:
    print("1. Avg Temp")
    print("2. Avg Humidity")
    print("3. Print all Rows")
    print("0. Exit")
    userInput = input()
    if userInput == 1:
        print("Avg. Temp = " + str(sql.avgTemp()))
    elif userInput == 2:
        print("Avg. Humidity = " + str(sql.avgHumidity()))
    elif userInput == 3:
        sql.getAllReadings()
    elif userInput != 0:
        print("Invalid input")