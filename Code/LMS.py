"""
File: LMS.py

Description: LMS Data Collector
	Send serial commands to set up the LiDAR device. 
	
	Collects a new set of data every 1 second
	and saves the data to a thread-safe stack. 
"""

# How to Configure
# 1. Power On
# 2. LMS291 Sends "power-on" string
# 3. Send "installation mode" string (20h)
# 4. Acknowledge (06h)
# 5. Response(A0h)
# 6. Set parameters
# 7. Acknowledge (06h)
# 8. Response (F7h)
# 9. Switch to monitoring mode (20h)
# 10. Acknowledge (06h)
# 11. Response (A0h)
# 12. Wait for next request (eg. Start data transmission)

# How to run with default settings
# 1. Power On
# 2. LMS291 Sends "power-on" string
# 3. Send "send data" command
# 4. Acknowledge (06h)
# 5. Response
# 6. Wait for next request (eg. Start data transmission)

import time
import logging
import serial
import binascii
import math
import numpy as np
from threading import Thread

class LMS(Thread):
	def __init__(self, lms_stack, lms_n, lms_s, device_path, stop):
		# Call Thread initializer
		super(LMS, self).__init__()
			
		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")

		# Save stack and semaphores
		self.lms_stack = lms_stack
		self.lms_n = lms_n
		self.lms_s = lms_s
		self.stop = stop
		
		# Open serial port for the device		
		self.ser = serial.Serial(
			port=device_path,
			baudrate=38400,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)

		self.config = 0
		self.count = 0
		
		setup()

	def setup(self):
		while self.config == 0:
			response = self.ser.read()
			if binascii.hexlify(response) == b'':
				self.logger.debug('. . .')
				self.count += 1
			if self.count == 5:
				self.ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
				self.count = 0

			if binascii.hexlify(response) == b'06':
				time1 = time.time()
				self.logger.debug('Command Acknowledged')

			if binascii.hexlify(response) == b'02':
				response = self.ser.read()
				if binascii.hexlify(response) == b'80':
					response = self.ser.readline()
					len = int(binascii.hexlify(response[1]+response[0]), 16)
					self.logger.debug('Length: ' + str(len))
					#self.logger.debug('Response: ' + binascii.hexlify(response[2]))
					#self.logger.debug('Status: ' + binascii.hexlify(response[len+1]))
					#self.logger.debug('Data: ' + binascii.hexlify(response[3:len+1]))

					if binascii.hexlify(response[2]) == b'90':
						self.logger.debug('LMS291 Powered On')
						#self.ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
						#self.config = 1

					elif binascii.hexlify(response[2]) == b'b1':
						self.logger.debug('LMS291 Connection Status Verified: ' + response[3:10])
						#self.ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode

						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180-0.5 degree variant

						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x64,0x00,0x1D,0x0F])) # 100-1 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x32,0x00,0xB1,0x59])) # 100-0.5 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x19,0x00,0xE7,0x72])) # 100-0.25 degree variant

						#self.config = 1

					elif binascii.hexlify(response[2]) == b'a0':
						self.logger.debug('LMS291 Installation Mode')
						#self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x40,0x50,0x08])) # Switch to 38,400 Bd
						#self.config = 1
					elif binascii.hexlify(response[2]) == b'bb':
						self.logger.debug('LMS291 Variant Switch')
						if binascii.hexlify(response[3]) == b'01':
							self.logger.debug('Switchover successful: ' + str(int(binascii.hexlify(response[4]),16)) + ' by ' + str(int(binascii.hexlify(response[6]),16)/100) + ' degrees')
							ang_start = (180-int(binascii.hexlify(response[4]),16))/2
							ang_inc = int(binascii.hexlify(response[6]),16)/100
							self.config = 1
						else:
							self.logger.debug('Switchover failed')

	def run(self):
		while self.config == 1:
			#self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x36,0x02,0x3E,0x1E])) # Mean Measured Data
			self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
			response = self.ser.read()
			if binascii.hexlify(response) == b'02':
				response=self.ser.read()
				if binascii.hexlify(response) == b'80':
					len_low = self.ser.read()
					len_high = self.ser.read()
					len = int(binascii.hexlify(len_high+len_low), 16)
					response = self.ser.read()
					self.logger.debug('Response: ' + binascii.hexlify(response))
					num_low = self.ser.read()
					num_high = self.ser.read()
					if int(binascii.hexlify(num_high),16)&int('0x40',16) == 0:
						unit = ' cm '
					else:
						unit = ' mm '
					num = int(binascii.hexlify(num_high+num_low),16)&int('0x3FFF',16)
					self.logger.debug('Number of points: ' + str(num))

					ang = ang_start
					data = [0] * (num+1)	# The actual data read from the LMS
					x = [0] * (num+1)		# x and y are the cartesian coordinate of the read data
					y = [0] * (num+1)
					r = [0] * (num+1)		# r and theta are the polar coordinates of the read data
					theta = [0] * (num+1)

					for i in range(1, num+1):
						data_low = self.ser.read()
						data_high = self.ser.read()
						data[i]=int(binascii.hexlify(data_high+data_low),16)
						
						# Save the data in polar form
						r[i] = data[i]
						theta[i] = ang*np.pi/180

						# Save the data in rectangular form
						x[i] = data[i]*math.cos(ang*(np.pi/180))
						y[i] = data[i]*math.sin(ang*(np.pi/180))

						ang += ang_inc

					# Finished data transmission, pick up final message
					status = self.ser.read()
					self.logger.debug('Status: ' + binascii.hexlify(status))
					response = self.ser.readline()
					self.logger.debug('Checksum: ' + binascii.hexlify(response))
					time2 = time.time()
					self.logger.debug(str(time2-time1)+' seconds')

					# Save data on the stack
					self.lms_s.acquire()
					self.lms_stack.append(r)
					self.lms_stack.append(theta)
					self.lms_s.release()
					self.lms_n.release()

					if self.stop:
						break