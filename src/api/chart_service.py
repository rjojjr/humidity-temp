from api.dht.read import Read
from api.dht.MySql import MySql
import datetime
from api.models.summary import Summary

from api.models.interval_request import IntervalRequest
from api.models.interval import Interval
from api.models.interval import Intervals
from api.models.records import ReadingRecord
from api.models.records import RoomSum

class ChartService:

    def __init__(self):
        self.sql = MySql()
        self.read = Read()
        self.daysInMonth = [
            31,
            28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31
        ]

    def getDayAvgApi(self, endRange, intervals, year, month, day, sdt, edt, rooms, interval):
        startTime = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = -1)).strftime('%Y-%m-%d %H:%M:%S')
        endTime = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = endRange)).strftime('%Y-%m-%d %H:%M:%S')
        records = self.sql.getRecordsBetween(startTime, endTime)
        records.sort(key=self._getDate)
        cursor = 0
        for k in range(0, endRange):
            if k % interval == 0:
                avgDate = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = k)).strftime('%Y-%m-%d %H:%M:%S')
                if day == 0:
                    sDate = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    sDate = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                eDate = (datetime.datetime(year, month, day, 0, 0, 0, 0) + datetime.timedelta(hours = (k + 1))).strftime('%Y-%m-%d %H:%M:%S')
                intervals.append(self._getInterval(records, cursor, sDate, eDate, avgDate, "temp", rooms).__dict__)

    def _getAvg(self, roomSums, room):
        for sum in roomSums:
            if sum.room == room:
                if sum.count == 0:
                    return None
                else:
                    return int(sum.sum / sum.count)
        return None

    def _getDate(self, reading):
        return reading.date

    def _addRoomReading(self, roomSums, reading, type):
        sums = []
        for tSum in roomSums:
            sum = tSum.sum
            count = tSum.count
            if tSum.room == reading.room:
                if type == "temp":
                    sum = tSum.sum + reading.temp
                else:
                    sum = tSum.sum + reading.humidity
                count = tSum.count + 1
            sums.append(RoomSum(tSum.room, sum, count))
        return sums

    def _splitDate(self, date):
        split = []
        days = str(date).split(" ")[0]
        hours = str(date).split(" ")[1]
        for unit in days.split("-"):
            split.append(int(unit))
        for unit in hours.split(":"):
            split.append(int(unit))
        return split

    def _compareDateSplit(self, subject, start, end):
        if str(subject) >= str(start) and str(subject) <= str(end):
            return True
        else:
            return False

    def _getInterval(self, readings, cursor, startDate, endDate, intervalDate, type, rooms):
        roomSums = []
        for room in rooms:
            roomSums.append(RoomSum(room, 0, 0))
        first = True
        count = 0
        for i in range(cursor, len(readings)):
            count = count + 1
            if self._compareDateSplit(readings[i].date, startDate, endDate):
                if first:
                    first = False
                roomSums = self._addRoomReading(roomSums, readings[i], type)
            else:
                if first == False:
                    break
        cursor = cursor + count
        return Interval(intervalDate, self._getAvg(roomSums, "office"), self._getAvg(roomSums, "bedroom"), self._getAvg(roomSums, "freezer"), self._getAvg(roomSums, "outside"))
