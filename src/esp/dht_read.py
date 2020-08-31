import Adafruit_DHT
from machine import Pin

dhtDevice = Adafruit_DHT.DHT22(board.D15)

def read():
    print('reading...')
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print('temp: ' + str(temperature) + ' humidity: ' + str(humidity))
    temp = (1.8 * temperature) + 32
    return [str(temp), str(humidity)]