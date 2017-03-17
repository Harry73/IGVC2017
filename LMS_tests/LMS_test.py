

import time
import serial
import binascii #note that this needs to be updated for python3
import math
import numpy as np
from threading import Thread

class LMS_test(Thread):

	def __init__(self, lms_data_stack, lms_n, lms_s, device_path):
		# Call Thread initializer
		super(LMS_test, self).__init__()

		self.lms_data_stack = lms_data_stack
		self.lms_n = lms_n
		self.lms_s = lms_s
		self.stopped = False

		# Set up serial port
		self.ser = serial.Serial(
			port = device_path,
			baudrate = 38400,
			parity =serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout = 1
		)
		
		config = 0
		while config == 0:
			response = self.ser.read()
			if binascii.hexlify(response) == b'':
				print('. . .')
				count += 1
			if count == 5:
				self.ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
				count = 0

			if binascii.hexlify(response) == b'06':
				time1 = time.time()
				print('Command Acknowledged')

			if binascii.hexlify(response) == b'02':
				response = self.ser.read()
				if binascii.hexlify(response) == b'80':
					response = self.ser.readline()
					len = int(binascii.hexlify(response[1]+response[0]), 16)
					print('Length: ' + str(len))
					#print('Response: ' + binascii.hexlify(response[2]))
					#print('Status: ' + binascii.hexlify(response[len+1]))
					#print('Data: ' + binascii.hexlify(response[3:len+1]))

					if binascii.hexlify(response[2]) == b'90':
						print('LMS291 Powered On')
						#self.ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant

					elif binascii.hexlify(response[2]) == b'b1':
						print('LMS291 Connection Status Verified: ' + response[3:10])
						#self.ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode

						self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180-0.5 degree variant

						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x64,0x00,0x1D,0x0F])) # 100-1 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x32,0x00,0xB1,0x59])) # 100-0.5 degree variant
						#self.ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x19,0x00,0xE7,0x72])) # 100-0.25 degree variant

					elif binascii.hexlify(response[2]) == b'a0':
						print('LMS291 Installation Mode')
						#self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x40,0x50,0x08])) # Switch to 38,400 Bd

					elif binascii.hexlify(response[2]) == b'bb':
						print('LMS291 Variant Switch')
						if binascii.hexlify(response[3]) == b'01':
							print('Switchover successful: ' + str(int(binascii.hexlify(response[4]), 16)) + ' by ' + str(int(binascii.hexlify(response[6]), 16)/100) + ' degrees')
							self.ang_start = (180-int(binascii.hexlify(response[4]), 16))/2
							self.ang_inc = int(binascii.hexlify(response[6]), 16)/100
							config = 1	# Setup complete
						else:
							print('Switchover failed')

	# Scans based on settings and returns values in an array
	def scan(self):
		self.ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
		response = self.ser.read()
		if binascii.hexlify(response) == b'02':
			response = self.ser.read()
			if binascii.hexlify(response) == b'80':
				len_low = self.ser.read()
				len_high = self.ser.read()
				len = int(binascii.hexlify(len_high+len_low), 16)
				response = self.ser.read()
				print('Response: ' + binascii.hexlify(response))
				num_low = self.ser.read()
				num_high = self.ser.read()
				if int(binascii.hexlify(num_high), 16) & int('0x40', 16) == 0:
					unit = ' cm '
				else:
					unit = ' mm '
				num = int(binascii.hexlify(num_high+num_low), 16) & int('0x3FFF', 16)
				print('Number of points: ' + str(num))

				data = [0] * (num+1)	# The actual data read from the LMS

				print("Reading data")
				for i in range(1, num+1):
					data_low = self.ser.read()
					data_high = self.ser.read()
					data[i] = int(binascii.hexlify(data_high+data_low), 16)
					
				# Finished data transmission, pick up final message
				status = self.ser.read()
				print('Status: ' + binascii.hexlify(status))
				response = self.ser.readline()
				print('Checksum: ' + binascii.hexlify(response))
				time2 = time.time()
				print(str(time2-time1) + ' seconds')

				return data

	def run(self):
		# Run until the Driver calls for a stop
		while not self.stopped:
			# Get data from LMS
			data = self.scan()

			# Push the data on the stack thread-safely
			self.lms_s.acquire()
			self.lms_data_stack.append(data)
			self.lms_s.release()
			self.lms_n.release()
		
	def stop(self):
		self.stopped = True
				
# Test run
if __name__ == "__main__":
	from threading import Semaphore
	
	lms_data_stack = []
	lms = LMS_test(lms_data_stack, Semaphore(0), Semaphore(1), "/dev/ttyUSB0")
	
	lms.start()
	
	time.sleep(10)
	
	lms.stop()
	lms.join()
	
	for set in lms_data_stack:
		print(set)
		print("---------------------------")