class Summary:
    def __init__(self, now, day, week, sensor=None, lastUpdate=None):
        self.now = now
        self.day = day
        self.week = week
        if sensor is None:
            self.sensor = ""
        else:
            self.sensor = sensor
        if lastUpdate is None:
            self.lastUpdate = ""
        else:
            self.lastUpdate = lastUpdate