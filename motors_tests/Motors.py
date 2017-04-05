import wiringpi2 as wpi
from threading import Thread

# Low level functionality to use wiringpi2 to control 
# steering and drive motors
class Motors(Thread):

	# Initial setup
	def __init__(self):
		super(Motors, self).__init__()
		wpi.wiringPiSetup()

		self.drive_pin = 4
		wpi.pinMode(self.drive_pin, 1)
		wpi.digitalWrite(self.drive_pin, 0)
		
		self.steering_pin = 21
		wpi.pinMode(self.steering_pin, 1)
		wpi.digitalWrite(self.steering_pin, 0)
		self.steering_frequency = int(1/60*1000000)	# 60 Hz
		self.steering_pulse = 1000
		
		self.stopped = 1	# Motors are initially stopped

	# Steering servo requires a pulse-width modulated signal, which the thread generates continuously
	def run(self):
		while True:
			if self.stopped == 1:
				pass
			elif self.stopped == 0:
				wpi.digitalWrite(self.steering_pin, 1)
				wpi.delayMicroseconds(self.steering_pulse)
				wpi.digitalWrite(self.steering_pin, 0)
				wpi.delayMicroseconds(self.steering_frequency - self.steering_pulse)
			else:
				break
	
	# Change the width of the steering pulse
	def turn(self, pulse):
		self.steering_pulse = pulse

	# Send a single pulse signal to the drive motor
	def drive(self, drive_pulse):
		wpi.digitalWrite(self.drive_pin, 1)
		wpi.delayMicroseconds(drive_pulse)
		wpi.digitalWrite(self.drive_pin, 0)
		
	def restart(self):
		self.stopped = 0
		
	# Terminate the thread
	def stop(self):
		self.stopped = 1
		
	def terminate(self):
		self.stopped = -1
