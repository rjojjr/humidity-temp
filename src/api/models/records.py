class ReadingRecord:
    def __init__(self, room, temp, humidity, date):
        self.room = room
        self.temp = temp
        self.humidity = humidity
        self.date = date

class RoomSum:
    def __init__(self, room, sum, count):
        self.room = room
        self.sum = sum
        self.count = count