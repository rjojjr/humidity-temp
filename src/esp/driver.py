import dht_read
import send
import time

def main():
    time.sleep(15)
    while True:
        reading = dht_read.read()
        send.http_send(reading[0], reading[1], "outside")
        time.sleep(15)