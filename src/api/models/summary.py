class Summary:
    def __init__(self, now, day, week, sensor=None):
        self.now = now
        self.day = day
        self.week = week
        if sensor is None:
            self.sensor = ""
        else:
            self.sensor = sensor