"""
File: LMS.py

Description: LMS Data Collector
	Send serial commands to set up the LiDAR device.

	Collects a new set of data every 1 second
	and saves the data to a thread-safe stack.
"""

import time
import serial
import math
import logging
import binascii
import numpy as np
from multiprocessing import Process, Queue

class LMS(Process):

	def __init__(self, lms_data_stack, lms_n, lms_s, device_path):
		# Call Process initializer
		super(LMS, self).__init__()

		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")

		# Save stack and semaphores
		self.lms_data_stack = lms_data_stack
		self.lms_n = lms_n
		self.lms_s = lms_s
		self.stopped = Queue()

		# Set up serial port
		self.ser = serial.Serial(
			port = device_path,
			baudrate = 38400,
			parity =serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout = 1
		)

		count = 0
		config = 0
		while config == 0:
			response = self.ser.read()
			if binascii.hexlify(response) == b'':
				logging.debug('Waiting for LiDAR...')
				count += 1
			if count == 5:
				self.ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
				count = 0

			if binascii.hexlify(response) == b'06':
				logging.debug('LiDAR command acknowledged')

			if binascii.hexlify(response) == b'02':
				response = self.ser.read()
				if binascii.hexlify(response) == b'80':
					response = self.ser.readline()
					response2 = "{0:x}".format(response[2])

					if response2 == '90':
						logging.debug('LiDAR Powered On')
						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant

					elif response2 == 'b1':
						logging.debug('LiDAR Connection Status Verified: ' + str(response[3:10]))

						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant

					elif response2 == 'a0':
						logging.debug('LiDAR Installation Mode')

					elif response2 == 'bb':
						logging.debug('LiDAR Variant Switch')
						if "{0:x}".format(response[3]) == '1':
							logging.debug('LiDAR switchover successful: {0:x} by {1:x} degrees'.format(response[4], response[6]))
							self.ang_start = (180-int(str(response[4]), 16))/2
							self.ang_inc = int(str(response[6]), 16)/100
							config = 1	# Setup complete
						else:
							logging.error('LiDAR switchover failed')

	# Scans based on settings and returns values in an array
	def run(self):
		# Run until the Driver calls for a stop
		while self.stopped.empty():
			self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
			response = self.ser.read()

			if binascii.hexlify(response) == b'02':
				response = self.ser.read()
				if binascii.hexlify(response) == b'80':
					len_low = self.ser.read()
					len_high = self.ser.read()
					response = self.ser.read()
					num_low = self.ser.read()
					num_high = self.ser.read()
					if int(binascii.hexlify(num_high), 16) & int('0x40', 16) == 0:
						unit = ' cm '
					else:
						unit = ' mm '
					num = int(binascii.hexlify(num_high+num_low), 16) & int('0x3FFF', 16)

					data = [0] * (num)	# The actual data read from the LMS

					for i in range(0, num):
						data_low = self.ser.read()
						data_high = self.ser.read()
						data[i] = int(binascii.hexlify(data_high+data_low), 16)/10

					# Finished data transmission, pick up final message
					status = self.ser.read()
					response = self.ser.readline()
					
					# Push the data on the stack thread-safely
					self.lms_s.acquire()
					self.lms_data_stack.append(data)
					self.lms_s.release()
					self.lms_n.release()

	def stop(self):
		self.stopped.put(True)

# Test run
if __name__ == "__main__":
	import os
	from multiprocessing import Semaphore, Manager

	lms_data_stack = Manager().list()
	lms = LMS(lms_data_stack, Semaphore(0), Semaphore(1), "/dev/" + os.readlink("/dev/IGVC_LIDAR"))

	lms.start()

	time.sleep(10)

	lms.stop()
	lms.join()

	for set in lms_data_stack:
		print(set)
		print("---------------------------")
