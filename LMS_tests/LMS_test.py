

import time
import serial
import binascii #note that this needs to be updated for python3
import math 
import numpy as np

class LMS_test

def __init__(self):

	ser = serial.Serial(

	port='/dev/ttyUSB0',
		baudrate = 38400,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)
	while config==0:
	    response=ser.read()
	    if binascii.hexlify(response)==b'':
		print('. . .')
		count += 1
	    if count == 5:
		ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
		count = 0

	    if binascii.hexlify(response)==b'06':
		time1 = time.time()
		print('Command Acknowledged')

	    if binascii.hexlify(response)==b'02':
		response=ser.read()
		if binascii.hexlify(response)==b'80':
		    response=ser.readline()
		    len = int(binascii.hexlify(response[1]+response[0]), 16)
		    print('Length: ' + str(len))
		    #print('Response: ' + binascii.hexlify(response[2]))
		    #print('Status: ' + binascii.hexlify(response[len+1]))
		    #print('Data: ' + binascii.hexlify(response[3:len+1]))

		    if binascii.hexlify(response[2])==b'90':
		        print('LMS291 Powered On')
		        #ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
		        ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
		        #config = 1

		    elif binascii.hexlify(response[2])==b'b1':
		        print('LMS291 Connection Status Verified: ' + response[3:10])
		        #ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode

		        ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
		        #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180-0.5 degree variant

		        #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x64,0x00,0x1D,0x0F])) # 100-1 degree variant
		        #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x32,0x00,0xB1,0x59])) # 100-0.5 degree variant
		        #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x19,0x00,0xE7,0x72])) # 100-0.25 degree variant

		        #config = 1

		    elif binascii.hexlify(response[2])==b'a0':
		        print('LMS291 Installation Mode')
		        #ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x40,0x50,0x08])) # Switch to 38,400 Bd
		        #config = 1
		    elif binascii.hexlify(response[2])==b'bb':
		        print('LMS291 Variant Switch')
		        if binascii.hexlify(response[3])==b'01':
		            print('Switchover successful: ' + str(int(binascii.hexlify(response[4]),16)) + ' by ' + str(int(binascii.hexlify(response[6]),16)/100) + ' degrees')
		            ang_start = (180-int(binascii.hexlify(response[4]),16))/2
		            ang_inc = int(binascii.hexlify(response[6]),16)/100
		            config = 1
		        else:
		            print('Switchover failed')

#scans based on settings and returns values in an array
def scan(self):
	#ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x36,0x02,0x3E,0x1E])) # Mean Measured Data
	ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
	response=ser.read()
	if binascii.hexlify(response)==b'02':
		response=ser.read()
		if binascii.hexlify(response)==b'80':
			len_low=ser.read()
			len_high=ser.read()
			len = int(binascii.hexlify(len_high+len_low), 16)
			response=ser.read()
			print('Response: ' + binascii.hexlify(response))
			num_low=ser.read()
			num_high=ser.read()
			if int(binascii.hexlify(num_high),16)&int('0x40',16)==0:
		        	unit = ' cm '
			else:
			        unit = ' mm '
			num=int(binascii.hexlify(num_high+num_low),16)&int('0x3FFF',16)
			print('Number of points: ' + str(num))

		 	ang = ang_start
		 	data = [0] * (num+1)	# The actual data read from the LMS
			#x = [0] * (num+1)	# x and y are the cartesian coordinate of the read data
			#y = [0] * (num+1)
			#r = [0] * (num+1)	# r and theta are the polar coordinates of the read data
			#theta = [0] * (num+1)

			for i in range(1, num+1):
		        	data_low=ser.read()
		        	data_high=ser.read()
		        	data[i]=int(binascii.hexlify(data_high+data_low),16)
		        	print(str(i) + ': ' + str(data[i]) + unit + '@ ' + str(ang) + ' degrees')

		        	## Save the data in polar form
		        	#r[i] = data[i]
		        	#theta[i] = ang*np.pi/180

		        	# Save the data in rectangular form
		        	#x[i] = data[i]*math.cos(ang*(np.pi/180))
		        	#y[i] = data[i]*math.sin(ang*(np.pi/180))

		        	ang += ang_inc

		    	# Finished data transmission, pick up final message
		    	status=ser.read()
		    	print('Status: ' + binascii.hexlify(status))
		    	response=ser.readline()
		    	print('Checksum: ' + binascii.hexlify(response))
		    	time2 = time.time()
		    	print(str(time2-time1)+' seconds')

			return data
		
		
	
	
