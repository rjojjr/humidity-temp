from api.dht.read import Read
from api.dht.MySql import MySql
import datetime
from api.models.summary import Summary

from api.models.interval_request import IntervalRequest
from api.models.interval import Interval
from api.models.interval import Intervals
from api.chart_service import ChartService

class SummaryService:

    def __init__(self):
        self.sql = MySql()
        self.read = Read()
        self.chartService = ChartService()
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
            return Intervals(self.getTempAvgChart(intervalRequest)).__dict__
        else:
            return Intervals(self.getTempDiffChart(intervalRequest)).__dict__
        return []

    def getTempAvgChart(self, intervalRequest):
        intervals = []
        sdt = intervalRequest.startDate.split("-")
        edt = intervalRequest.endDate.split("-")
        if int(sdt[0]) == int(edt[0]):
            self.getAvgIntervals("avg", intervals, int(sdt[0]), sdt, edt)
        else:
            for j in range(int(sdt[0]), int(edt[0])):
                self.getAvgIntervals("avg", intervals, j, sdt, edt)
        return intervals

    def getTempDiffChart(self, intervalRequest):
        intervals = []
        sdt = intervalRequest.startDate.split("-")
        edt = intervalRequest.endDate.split("-")
        if intervalRequest.startDate == intervalRequest.endDate:
            for k in range(0, 25):
                if ((k % 2) == 0):
                    avgDate = (datetime.datetime(int(sdt[0]), int(sdt[1]), int(sdt[2]), 0, 0) + datetime.timedelta(hours = k)).strftime('%Y-%m-%d %H:%M:%S')
                    if k == 0:
                        sDate = (datetime.datetime(int(sdt[0]), int(sdt[1]), int(sdt[2]), 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        sDate = (datetime.datetime(int(sdt[0]), int(sdt[1]), int(sdt[2]), 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                    eDate = (datetime.datetime(int(sdt[0]), int(sdt[1]), int(sdt[2]), 0, 0) + datetime.timedelta(hours = (k + 1))).strftime('%Y-%m-%d %H:%M:%S')
                    office = self.sql.tempDiffBetween("office", sDate, eDate)
                    bedroom = self.sql.tempDiffBetween("bedroom", sDate, eDate)
                    freezer = self.sql.tempDiffBetween("freezer", sDate, eDate)
                    outside = self.sql.tempDiffBetween("outside", sDate, eDate)
                    interval = Interval(avgDate, [str(office[0]), str(office[1])], [str(bedroom[0]), str(bedroom[1])], [str(freezer[0]), str(freezer[1])], [str(outside[0]), str(outside[1])])
                    intervals.append(interval.__dict__)
        else:
            if int(sdt[0]) == int(edt[0]):
                self.getAvgIntervals("diff", intervals, int(sdt[0]), sdt, edt)
            else:
                for j in range(int(sdt[0]), int(edt[0])):
                    self.getAvgIntervals("diff", intervals, j, sdt, edt)
        return intervals

    def getAvgIntervals(self, type, intervals, j, sdt, edt):
        if int(edt[0]) == j and int(sdt[0]) == int(edt[0]):
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
            self.getMonthAvg(type, intervals, j, sMonth, sdt, edt)
        else:
            for q in range(sMonth, eMonth + 1):
                self.getMonthAvg(type, intervals, j, q, sdt, edt)

    def getMonthAvg(self, type, intervals, j, q, sdt, edt):
        rooms = self.sql.getRooms()
        if int(edt[1]) == q and int(edt[0]) == j and int(sdt[0]) == j and int(sdt[1]) == q:
            sDay = int(sdt[2])
            eDay = int(edt[2])
        elif int(edt[1]) == q and int(edt[0]) == j:
            sDay = 1
            eDay = int(edt[2])
        else:
            sDay = 1
            eDay = self.daysInMonth[q]
        if sDay == eDay:
            if type == "avg":
                self.chartService.getDayAvgApi(25, intervals, j, q, sDay, sdt, edt, rooms, 2)
            else:
                self.getDayDiff(intervals, j, q, sDay, sdt, edt)
        else:
            for i in range(sDay, eDay + 1):
                if i == eDay:
                    if type == "avg":
                        self.chartService.getDayAvgApi(25, intervals, j, q, i, sdt, edt, rooms, 6)
                    else:
                        self.getDayDiff(24, intervals, j, q, i, sdt, edt)
                else:
                    if type == "avg":
                        self.chartService.getDayAvgApi(25, intervals, j, q, i, sdt, edt, rooms, 6)
                    else:
                        self.getDayDiff(23, intervals, j, q, i, sdt, edt)

    def getDayAvg(self, endRange, intervals, j, q, i, sdt, edt):
        for k in range(0, endRange):
                avgDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = k)).strftime('%Y-%m-%d %H:%M:%S')
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

    def getDayDiff(self, endRange, intervals, j, q, i, sdt, edt):
        for k in range(0, endRange):
            if ((k % 6) == 0):
                avgDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = k)).strftime('%Y-%m-%d %H:%M:%S')
                if i == 0:
                    sDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    sDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k - 1))).strftime('%Y-%m-%d %H:%M:%S')
                eDate = (datetime.datetime(j, q, i, 0, 0, 0, 0) + datetime.timedelta(hours = (k + 1))).strftime('%Y-%m-%d %H:%M:%S')
                office = self.sql.tempDiffBetween("office", sDate, eDate)
                bedroom = self.sql.tempDiffBetween("bedroom", sDate, eDate)
                freezer = self.sql.tempDiffBetween("freezer", sDate, eDate)
                outside = self.sql.tempDiffBetween("outside", sDate, eDate)
                interval = Interval(avgDate, [str(office[0]), str(office[1])], [str(bedroom[0]), str(bedroom[1])], [str(freezer[0]), str(freezer[1])], [str(outside[0]), str(outside[1])])
                intervals.append(interval.__dict__)