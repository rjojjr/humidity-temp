from api.dht.read import Read
from api.dht.MySql import MySql
import datetime
from api.models.summary import Summary

from api.models.interval_request import IntervalRequest
from api.models.interval import Interval
from api.models.interval import Intervals

class SummaryService:

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

    def getSlaveSummary(self, room):
        now = self.read.getTemp()
        day = [str(self.sql.avgTempToday(room)), str(self.sql.avgHumidityToday(room))]
        nowTime = datetime.datetime.today() + datetime.timedelta(days = 1)
        weekTime = datetime.datetime.today() - datetime.timedelta(days = 7)
        week = [str(self.sql.avgTempBetween(room, weekTime.strftime('%Y-%m-%d'), nowTime.strftime('%Y-%m-%d'))), str(self.sql.avgHumidityBetween(room, weekTime.strftime('%Y-%m-%d'), nowTime.strftime('%Y-%m-%d')))]
        summary = Summary(now, day, week)
        return summary.__dict__

    def getSummary(self, room):
        latest = self.sql.latestReadingWithTime(room)
        now = [latest[0], latest[1]]
        day = [str(self.sql.avgTempToday(room)), str(self.sql.avgHumidityToday(room))]
        nowTime = datetime.datetime.today() + datetime.timedelta(days = 1)
        weekTime = datetime.datetime.today() - datetime.timedelta(days = 7)
        week = [str(self.sql.avgTempBetween(room, weekTime.strftime('%Y-%m-%d'), nowTime.strftime('%Y-%m-%d'))), str(self.sql.avgHumidityBetween(room, weekTime.strftime('%Y-%m-%d'), nowTime.strftime('%Y-%m-%d')))]
        summary = Summary(now, day, week, room, latest[2])
        return summary.__dict__

    def getSummaries(self, rooms):
         summaries = []
         for room in rooms:
            summaries.append(self.getSummary(room))
         return summaries

    def getSummaries(self):
          summaries = []
          for room in self.sql.getRooms():
             summaries.append(self.getSummary(room))
          return summaries

    def getChart(self, intervalRequest):
        if intervalRequest.type == "temp":
            return Intervals(self.getTempChart(intervalRequest)).__dict__
        return []

    def getTempChart(self, intervalRequest):
        intervals = []
        if intervalRequest.startDate == intervalRequest.endDate:
            dt = intervalRequest.startDate.split("-")
            for i in range(0, 23):
                if i % 2 == 0:
                    avgDate = (datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0) + datetime.timedelta(hours = i)).strftime('%Y-%m-%d %H:%M:%S')
                    if i == 0:
                        sDate = (datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0) + datetime.timedelta(hours = (i - 1))).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        sDate = (datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0) + datetime.timedelta(hours = (i - 1))).strftime('%Y-%m-%d %H:%M:%S')
                    eDate = (datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0) + datetime.timedelta(hours = (i + 1))).strftime('%Y-%m-%d %H:%M:%S')
                    office = self.sql.avgTempBetween("office", sDate, eDate)
                    bedroom = self.sql.avgTempBetween("bedroom", sDate, eDate)
                    freezer = self.sql.avgTempBetween("freezer", sDate, eDate)
                    outside = self.sql.avgTempBetween("outside", sDate, eDate)
                    interval = Interval(avgDate, str(office), str(bedroom), str(freezer), str(outside))
                    intervals.append(interval.__dict__)
        else:
            sdt = intervalRequest.startDate.split("-")
            edt = intervalRequest.endDate.split("-")
            if int(sdt[0]) == int(edt[0]):
                self.getIntervals(intervals, int(sdt[0]), sdt, edt)
            else:
                for j in range(int(sdt[0]), int(edt[0])):
                    self.getIntervals(intervals, j, sdt, edt)


        return intervals

    def getIntervals(self, intervals, j , sdt, edt):
        if int(edt[0]) == j & int(sdt[0]) == int(edt[0]):
            sMonth = int(sdt[1])
            eMonth = int(edt[1])
        elif int(edt[0]) == j:
            sMonth = 1
            eMonth = int(edt[1])
        elif int(sdt[0]) == j:
            sMonth = int(sdt[1])
            eMonth = 12
        else:
            sMonth = 1
            eMonth = 12
        if sMonth == eMonth:
            self.getMonth(intervals, j, sMonth, sdt, edt)
        else:
            for q in range(sMonth, eMonth):
                self.getMonth(intervals, j, q, sdt, edt)

    def getMonth(self, intervals, j, q, sdt, edt):
        if int(edt[1]) == q & int(edt[0]) == j & int(sdt[0]) == j & int(sdt[1]) == q:
            sDay = int(sdt[2])
            eDay = int(edt[2])
        elif int(edt[1]) == q & int(edt[0]) == j:
            sDay = 1
            eDay = int(edt[2])
        else:
            sDay = 1
            eDay = self.daysInMonth[q]
        if sDay == eDay:
            self.getDay(intervals, j, q, sDay, sdt, edt)
        else:
            for i in range(sDay, eDay):
                self.getDay(intervals, j, q, i, sdt, edt)

    def getDay(self, intervals, j, q, i, sdt, edt):
        avgDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = 0)).strftime('%Y-%m-%d %H:%M:%S')
        for k in range(0, 23):
            if ((k % 6) == 0):
                if i == 0:
                    sDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    sDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                eDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k + 1))).strftime('%Y-%m-%d %H:%M:%S')
                office = self.sql.avgTempBetween("office", sDate, eDate)
                bedroom = self.sql.avgTempBetween("bedroom", sDate, eDate)
                freezer = self.sql.avgTempBetween("freezer", sDate, eDate)
                outside = self.sql.avgTempBetween("outside", sDate, eDate)
                interval = Interval(avgDate, str(office), str(bedroom), str(freezer), str(outside))
                intervals.append(interval.__dict__)