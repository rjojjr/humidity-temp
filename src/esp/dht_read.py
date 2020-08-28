import dht
from machine import Pin

sensor = dht.DHT11(Pin(15))

def read():
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    temp = (1.8 * temperature) + 32
    return [f'{temp}', f'{humidity}']