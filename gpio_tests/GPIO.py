import time
import wiringpi2 as wpi
from threading import Thread

class Servo(Thread):

	def __init__(self, servo_pin):
		super(Servo, self).__init__()
		wpi.wiringPiSetup()

		self.pin = servo_pin
		wpi.pinMode(self.pin, 1)
		wpi.digitalWrite(self.pin, 0)

		self.stopped = 1
		self.frequency = int(1/60*1000000)	# 60 Hz
		self.pulse = 1000

	def run(self):
		while True:
			if self.stopped == 0:
				time.sleep(1)
			elif self.stopped == 1:
				pass
				wpi.digitalWrite(self.pin, 1)
				wpi.delayMicroseconds(self.pulse)
				wpi.digitalWrite(self.pin, 0)
				wpi.delayMicroseconds(self.frequency - self.pulse)
			else:
				break

	def signal(self, new_pulse):
		self.pulse = new_pulse

	def stop(self):
		self.stopped = -1

	def end(self):
		self.stopped = -1
		
# Helper functions for wiringpi2
def setup(pins):
	wpi.wiringPiSetup()
	for pin in pins:
		wpi.pinMode(pin, 1)
		
def write(pin):
	wpi.digitalWrite(pin, 1)
	
def clear(pin):
	wpi.digitalWrite(pin, 0)
	
def signal(pin, time):
	wpi.digitalWrite(pin, 1)
	wpi.delayMicroseconds(time)
	wpi.digitalWrite(pin, 0)
