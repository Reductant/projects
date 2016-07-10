#!/usr/bin/python3

import RPi.GPIO as gpio
import time
import datetime
import os
import picamera

directory = "/home/pi/myprograms/pir/"

sensor = 21
led = 4

#segments = (11, 4, 23, 8, 7, 10, 18, 25)

#digits = (22, 27, 17, 24)

camera = picamera.PiCamera()
camera.resolution = (2592,1944)
camera.hflip = True
camera.vflip = True

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(sensor, gpio.IN, gpio.PUD_UP)
gpio.setup(led, gpio.OUT)
gpio.output(led, 0)


previous_state = False
current_state = False

log = ""

t = datetime.datetime.now()
past_minute = t.minute


filecode = 0
try:
    while True:
        time.sleep(0.1)

        filestring = str(filecode)
        while len(filestring) < 4:
            filestring = "0" + filestring

        previous_state = current_state
        current_state = gpio.input(sensor)
        t = str(datetime.datetime.now())

        if current_state != previous_state:
            gpio.output(led, 1)
            new_state = "HIGH" if current_state else "LOW"
            if new_state == "HIGH":
                camera.capture(directory + filestring + " " +  t + ".jpg")
                filecode += 1
        else:
            gpio.output(led, 0)

        print(current_state)	


finally:
    gpio.cleanup()
