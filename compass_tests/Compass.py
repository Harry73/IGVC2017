#Compass program
#returns angle of vehicle

import smbus
import time
import math

class Compass():
	def __init__(self)
		bus = smbus.SMBus(0)
		#unsure if this is the correct address on the ODroid

		address = 0x00
		#some settings options

		write_byte(0,0b01110000) #8 samples @ 15Hz 

		write_byte(1,0b00100000) #1.3 gain LSb/Gauss 1090(default)
		write_byte(2,0b00000000) #Continuous sampling

		scale = 0.92
		#include offset values when calculated
		x_offset = 0
		y_offset = 0

		orientation()

	#reads data stored in a specified address
	def read_byte(adr):
		return bus.read_byte_data(address,adr)


	#reads data as a word from an address
	def read_word(adr):
		high = bus.read_byte_data(address,adr)
		low = bus.read_byte_data(address,adr+1)
		val = (high << 8) + low
		return val


	#reads data, uses a simple address from the i2c address location
	def read_word_2c(adr):
		val = read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else: 
			return val

	#writes a value to a specific address
	#used here mainly for settings
	def write_byte(adr,value):
		bus.write_byte_data(address,adr,value)

	#returns a more accurate bearing of the vehicle
	def orientation():
		x_out = (read_word_2c(3)-x_offset)*scale
		y_out = (read_word_2c(7)-y_offset)*scale
		z_out = read_word_2c(5)*scale

		bearing = math.atan2(y_out,x_out)
		if (bearing < 0):
			bearing += 2*math.pi

		return math.degrees(bearing)
