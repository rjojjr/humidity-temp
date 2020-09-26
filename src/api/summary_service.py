from api.dht.read import Read
from api.dht.MySql import MySql
import datetime
from api.models.summary import Summary

from api.models.interval_request import IntervalRequest
from api.models.interval import Interval

class SummaryService:

    def __init__(self):
        self.sql = MySql()
        self.read = Read()

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
        if (intervalRequest.type == "temp"):
            return getTempChart(intervalRequest)
        return []

    def getTempChart(self, intervalRequest):
        intervals = []
        if (intervalRequest.startDate == intervalRequest.endDate):
            for i in range(0, 23):
                sDate = date(startDate) + datetime.timedelta(hours = (i - 1))
                eDate = date(startDate) + datetime.timedelta(hours = (i + 1))
                office = self.sql.avgTempBetween("office", sDate, endDate)
                bedroom = self.sql.avgTempBetween("bedroom", sDate, endDate)
                freezer = self.sql.avgTempBetween("freezer", sDate, endDate)
                outside = self.sql.avgTempBetween("office", sDate, endDate)
                intervals.append(Interval(office, bedroom, freezer, outside))
                
        return intervals