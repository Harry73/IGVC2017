"""
File: Compass.py

Description: Compass Manager Module
	Interfaces with HMC5883L sensor using I2C and GPIO

Additional notes:
Requires python 3

Also requires the i2clibraries/ and quick2wire/ at the same level as this file. 
See links for these libraries

https://bitbucket.org/thinkbowl/i2clibraries.git
https://github.com/quick2wire/quick2wire-python-api

PythonPath environment variable should contain the path to quick2wire. 
	export QUICK2WIRE_API_HOME=[the directory cloned from Git or unpacked from the source archive]
	export PYTHONPATH=$PYTHONPATH:$QUICK2WIRE_API_HOME
On the odroid, this is set automatically in bash. 
"""

import time
import logging
from threading import Thread
from i2clibraries import i2c_hmc5883l

class Compass(Thread):
	def __init__(self, compass_stack, compass_n, compass_s):
		# Call Thread initializer
		super(Compass, self).__init__()
		
		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")
		
		# Save stack and semaphores
		self.compass_stack = compass_stack
		self.compass_n = compass_n
		self.compass_s = compass_s
		self.stopped = False
		
		# Instantiates compass
		self.compass = i2c_hmc5883l.i2c_hmc5883l(4)	# 4 is because /dev/i2c-4 is the GPIO I2C bus on the odroid
		self.compass.setContinuousMode()
		self.compass.setDeclination(0, 6)
	
	def run(self):
		# Run until Driver calls for a stop
		while not self.stopped:
			time.sleep(0.5)
			
			# Get data from compass
			heading = self.compass.getHeading()
			
			# Push the heading on the stack thread-safely
			self.compass_s.acquire()
			self.compass_stack.append(heading)
			self.compass_s.release()
			self.compass_n.release()

	def getHeading(self):
		return self.compass.getHeading()
		
	# Tell run() to end
	def stop(self):
		self.stopped = True