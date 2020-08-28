import dht
from machine import Pin

sensor = dht.DHT11(Pin(15))

def read():
    print('reading...')
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print('temp: ' + str(temperature) + ' humidity: ' + str(humidity))
    temp = (1.8 * temperature) + 32
    return [str(temp), str(humidity)]