# Readme

This project uses a Raspberry Pi with DHT22 digital temp and humidity sensor and TM1637 LED display.

## Install Dependencies

```$xslt
sudo apt-get install python-dev python-pip
sudo pip install wiringpi2
sudo pip install Adafruit_DHT
```

## Running

To run the program, launch temp.sh

You must run sh script with sudo to gain access to GPIO

```$xslt
bash temp.sh
```