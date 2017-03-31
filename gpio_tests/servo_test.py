import time
import wiringpi2 as wpi
from threading import Thread

class Servo(Thread):

	def __init__(self):
		super(Servo, self).__init__()
		wpi.wiringPiSetup()

		self.pin = 21
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
				wpi.delayMicroseconds(frequency - pulse)
			else:
				break

	def signal(self, new_pulse):
		if new_pulse >= 500 and new_pulse <= 1500:
			self.pulse = new_pulse

	def stop(self):
		self.stopped = 0

	def end(self):
		self.stopped = -1
		