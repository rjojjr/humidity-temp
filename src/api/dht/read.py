import api.dht.Adafruit_DHT

DHT_PIN = 4

class Read:
    def getTemp(self):
        sensor = Adafruit_DHT.DHT22
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
        temp = (1.8 * temperature) + 32
        humidity = humidity
        t = str((temp))
        h = str((humidity))
        return [t, h]

    def dummy(self):
        return ["70", "60"]