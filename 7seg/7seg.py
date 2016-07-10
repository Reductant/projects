import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

segments = (11, 4, 23, 8, 7, 10, 18, 25)

digits = (22, 27, 17, 24)

for segment in segments:
	gpio.setup(segment, gpio.OUT)
	gpio.output(segment, 0)

for digit in digits:
	gpio.setup(digit, gpio.OUT)
	gpio.output(digit, 1)


num = {" ":(0,0,0,0,0,0,0),
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

try:
	while True:
		n = time.ctime()[11:13]+time.ctime()[14:16]
		s = str(n).rjust(4)
		print(s)
		for digit in range(4):
			for loop in range(0,7):
				gpio.output(segments[loop], num[s[digit]][loop])
				if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
					gpio.output(25, 1)
				else:
					gpio.output(25, 0)
			gpio.output(digits[digit], 0)
			time.sleep(0.001)
			gpio.output(digits[digit], 1)

finally:
	gpio.cleanup()
