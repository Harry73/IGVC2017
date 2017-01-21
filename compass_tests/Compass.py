#Compass program
#returns angle of vehicle

# sudo apt-get install python-smbus

import smbus
import time
import math

class Compass():
	def __init__(self)
		self.bus = smbus.SMBus(0)
		#unsure if this is the correct address on the ODroid

		self.address = 0x00
		#some settings options

		self.write_byte(0,0b01110000) #8 samples @ 15Hz 

		self.write_byte(1,0b00100000) #1.3 gain LSb/Gauss 1090(default)
		self.write_byte(2,0b00000000) #Continuous sampling

		self.scale = 0.92
		#include offset values when calculated
		self.x_offset = 0
		self.y_offset = 0

		self.orientation()

	#reads data stored in a specified address
	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address,adr)


	#reads data as a word from an address
	def read_word(self, adr):
		high = self.bus.read_byte_data(self.address,adr)
		low = self.bus.read_byte_data(self.address,adr+1)
		val = (high << 8) + low
		return val


	#reads data, uses a simple address from the i2c address location
	def read_word_2c(self, adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else: 
			return val

	#writes a value to a specific address
	#used here mainly for settings
	def write_byte(self, adr, value):
		self.bus.write_byte_data(self.address,adr,value)

	#returns a more accurate bearing of the vehicle
	def orientation(self):
		x_out = (self.read_word_2c(3)-self.x_offset)*self.scale
		y_out = (self.read_word_2c(7)-self.y_offset)*self.scale
		z_out = self.read_word_2c(5)*self.scale

		bearing = math.atan2(y_out,x_out)
		if (bearing < 0):
			bearing += 2*math.pi

		return math.degrees(bearing)
