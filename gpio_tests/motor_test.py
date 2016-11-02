import wiringpi2 as wpi
import time

wpi.wiringPiSetup()

pins = [1, 2]

for x in pins:
	wpi.pinMode(x, 1)
	wpi.digitalWrite(x, 0)

print("Start")

def signal(delay):
	wpi.digitalWrite(pins[0], 1)
	wpi.digitalWrite(pins[1], 1)
	wpi.delayMicroseconds(delay)
	wpi.digitalWrite(pins[0], 0)
	wpi.digitalWrite(pins[1], 0)


#wpi.digitalWrite(pins[0], 1)
#wpi.digitalWrite(pins[1], 1)
#wpi.delayMicroseconds(2000)
#wpi.digitalWrite(pins[0], 0)
#wpi.digitalWrite(pins[1], 0)

#while True:
#	pass
