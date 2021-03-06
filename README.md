# Readme

This project uses a Raspberry Pi running Ubuntu Server OS 
with DHT22 digital temp and humidity sensor and TM1637 LED display.

This project serves as a slave DHT22 API and will have a master API.

Project trello board can be found [here](https://trello.com/b/IbhfP8vr/py-temp)

You need the Trello improvements browser plugin to get story numbers.

Branches will be named "story-<story #>"

The readings will be stored in a MYSQL instance running in docker.

## Install Dependencies

### Docker

```$xslt
sudo apt install docker.io
```

### Python 

```$xslt
sudo apt-get install python-dev python-pip
sudo pip install wiringpi2
sudo pip install Adafruit_DHT
sudo pip install flask
pip install -U flask-cors
```

## MySQL

To pull and run the MySQL Docker container run:

```$xslt
docker run --name temp-mysql -v /hdd/mysql:/var/lib/mysql -e ALLOW_EMPTY_PASSWORD=1 -d mysql/mysql-server:latest
```

To access MySQL DB: 

```$xslt
docker exec -it temp-sql mysql -uroot
```

Now install python mysql connector

```$xslt
python -m pip install mysql-connector-python 
```

_*NOTE: You must MySQL v8 or above because older versions do not support ARM CPU*_

## Setup ESP32

Install esptool:

```$xslt
pip install esptool
```

Erase esp32's flash:

```$xslt
esptool.py --port /dev/ttyUSB0 erase_flash
```

Download latest micropython firmware and flash it:

```$xslt
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin
```

Install adafruit ampy

```
 pip3 install esptool adafruit-ampy
```

Move files in esp folder to esp Ex:

```
 ampy -p COM3 put src/esp/boot.py
```

## Running

To run the slave API, launch slave_api_main.py with room/sensor name argument.

_*NOTE: You must run as root to get access to GPIO*_

```$xslt
sudo python slave_api_main.py office
```
