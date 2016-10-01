#!/usr/bin/env python

import time
import serial
import binascii

ser = serial.Serial(

port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:
    response=ser.readline()
    print("0x" + str(binascii.hexlify(response[0:10])))

                        
