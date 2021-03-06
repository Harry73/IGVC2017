#!/usr/bin/env python

import time
import serial

ser = serial.Serial(

port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
#ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x24,0x34,0x08])) # Start continuous data
#ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x25,0x35,0x08])) # Stop continuous data
#ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
#ser.write(serial.to_bytes([0x02,0x00,0x21,0x00,0x77,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFC,0x7E])) # mm mode
#ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180,0.5 Degrees
