"""
import RPi.GPIO as gpio
import time
import datetime
import os
import picamera

directory = "/home/pi/myprograms/pir/"

sensor = 21

segments = (11, 4, 23, 8, 7, 10, 18, 25)

digits = (22, 27, 17, 24)

camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(sensor, gpio.IN, gpio.PUD_UP)

for segment in segments:
	gpio.setup(segment, gpio.OUT)
	gpio.output(segment, 0)

for digit in digits:
	gpio.setup(digit, gpio.OUT)
	gpio.output(digit, 0)

num = {
	" ":(0,0,0,0,0,0,0),
	"0":(1,1,1,1,1,1,0),
	"1":(0,1,1,0,0,0,0),
	"2":(1,1,0,1,1,0,1),
	"3":(1,1,1,1,0,0,1),
	"4":(0,1,1,0,0,1,1),
	"5":(1,0,1,1,0,1,1),
	"6":(1,0,1,1,1,1,1),
	"7":(1,1,1,0,0,0,0),
	"8":(1,1,1,1,1,1,1),
	"9":(1,1,1,1,0,1,1)}



previous_state = False
current_state = False

log = ""

t = datetime.datetime.now()
past_minute = t.minute


filecode = 0
try:
	while True:
		#time.sleep(0.1)

		filestring = str(filecode)
		while len(filestring) < 4:
			filestring = "0" + filestring

		previous_state = current_state
		current_state = gpio.input(sensor)
		t = str(datetime.datetime.now())

		if current_state != previous_state:
			new_state = "HIGH" if current_state else "LOW"		

			if new_state == "HIGH":
				camera.capture(directory + filestring + " " +  t + ".jpg")
				filecode += 1

		print(current_state)	

		for digit in range(4):
			for loop in range(0,7):
				gpio.output(segments[loop], num[filestring[digit]][loop])
			gpio.output(digits[digit], 0)
			time.sleep(0.001)
			gpio.output(digits[digit],1)

finally:
	gpio.cleanup()
