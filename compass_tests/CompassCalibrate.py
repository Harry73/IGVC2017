#Compass Calibration 

#Use this to find the xyz offsets required and put them in the designated spots in Compass.py
#remember to avoid metal and wiring when training the compass as it is sensitive to this equipment

import smbus
import time
import math

bus = smbus.SMBus(0)
#unsure if this is the correct address on the ODroid
address = 0x00

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

#some settings options
write_byte(0,0b01110000) #8 samples @ 15Hz 
write_byte(1,0b00100000) #1.3 gain LSb/Gauss 1090(default)
write_byte(2,0b00000000) #Continuous sampling

minx = 0
maxx = 0
miny = 0
maxy = 0
#finds the maxs and mins to find a correct offset amount
for i in range(0,500):
	x_out = read_word_2c(3)
	y_out = read_word_2c(7)
	z_out = read_word_2c(5)

	if x_out < minx:
		minx=x_out
	if y_out < miny:
		miny=y_out
	if x_out > maxx:
		maxx=x_out
	if y_out > maxy:
		maxy=y_out

#these go in the compass class
print "x offset: ", (maxx + minx)/2
print "y offset: ", (maxy + miny)/2
