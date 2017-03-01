"""
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
from i2clibraries import i2c_hmc5883l

def main():
	compass = i2c_hmc5883l.i2c_hmc5883l(4)	# 4 is because /dev/i2c-4 is the GPIO I2C bus on the odroid
	compass.setContinuousMode()
	compass.setDeclination(0, 6)
	
	# Get data from compass 10 times and print
	for i in range(10):
		print(compass)
		time.delay(1)
	
if __name__ == "__main__":
	main()
