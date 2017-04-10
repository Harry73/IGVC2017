"""
File: Motors.py

Description: Motor Controller
	Low level functionality to use wiringpi2 to control
	steering and drive motors. Provides methods to
	direct the steering and driving motors more simply.
"""

import wiringpi2 as wpi
from multiprocessing import Process, Queue

class Motors(Process):

	# Initial setup
	def __init__(self):
		super(Motors, self).__init__()
		wpi.wiringPiSetup()

		self.drive_pin = 23
		wpi.pinMode(self.drive_pin, 1)
		wpi.digitalWrite(self.drive_pin, 0)

		self.steering_pin = 21
		wpi.pinMode(self.steering_pin, 1)
		wpi.digitalWrite(self.steering_pin, 0)
		self.steering_frequency = int(1/60*1000000)	# 60 Hz
		self.steer_queue = Queue()
		self.steer_queue.put(1000)

		self.control_queue = Queue()
		self.control_queue.put(1)		# Thread is initially paused

	# Steering servo requires a pulse-width modulated signal, which the thread generates continuously
	def run(self):
		while True:
			if not self.control_queue.empty():
				self.stopped = self.control_queue.get()

			if not self.steer_queue.empty():
				self.steering_pulse = self.steer_queue.get()

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
		self.steer_queue.put(pulse)

	# Send a single pulse signal to the drive motor
	def drive(self, drive_pulse):
		wpi.digitalWrite(self.drive_pin, 1)
		wpi.delayMicroseconds(drive_pulse)
		wpi.digitalWrite(self.drive_pin, 0)

	# Unpause the thread
	def restart(self):
		self.control_queue.put(0)

	# Pause the thread
	def stop(self):
		self.drive(1360)
		self.control_queue.put(1)

	# Terminate the thread
	def terminate(self):
		self.drive(1360)
		self.control_queue.put(-1)
