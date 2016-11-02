#!/usr/bin/python3

import wiringpi2 as wpi
import time

wpi.wiringPiSetup()

pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 26, 27, 30, 31]

# GPIO pin setup
for x in pins:
	try:
		wpi.pinMode(x, 1)
		wpi.digitalWrite(x, 0)
		print("Pin #{0} set up".format(x))
	except:
		print("Pin  #{0} error".format(x))

print("done")
while True:
	wpi.digitalWrite(1, 0)
	wpi.delay(1)	# wait 1 millisecond
	wpi.digitalWrite(1, 1)
	wpi.delayMicroseconds(1000)	# wait 1 millisecond
