#!/usr/bin/env python

import time
import serial
import binascii
import math
import matplotlib.pyplot as plt

ser = serial.Serial(

port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

count = 0
mode = 1
check = 0
dataLen = [0] * 2
rawdata = [0] * 723
data_hex = [0] * 362
data = [0] * 362
out = [0] * 362
x = [0] * 362
y = [0] * 362
status = 0
mask = int('0xFFF8',16)
#mask = int('0x1FFF', 16)

while mode == 1: # Setup
    response=ser.readline()
    if binascii.hexlify(response[0:10])=='':
        print('. . .')
        print("0x" + str(binascii.hexlify(response[0:10])))

    count += 1
    if count == 10:
        ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
        count = 0
        
    if binascii.hexlify(response[0:10])=='02801700904c4d533239':
        print("LMS291: Powered On")
        ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command

    if binascii.hexlify(response[0:10])=='0602809a00b15830312e':
        print("LMS291: Connection Verified")
        ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode

    if binascii.hexlify(response[0:10])=='0602800300a00010160a':
        print("LMS291: Settings Mode")
        ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180,0.5 Degrees

    if binascii.hexlify(response[0:10])=='0602800700bb01b40032':
        print("LMS291: 180x0.5 Degrees")
        ser.write(serial.to_bytes([0x02,0x00,0x21,0x00,0x77,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFC,0x7E])) # mm mode

    if binascii.hexlify(response[0:10])=='0602802500f700000046':
        print("LMS291: mm Mode")
        print("LMS291: Start Data")
        ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x24,0x34,0x08])) # Start continuous data
        mode = 2

while mode == 2: # Wait for start bytes
    response=ser.read()
    #print("0x" + str(binascii.hexlify(response)) + "  " + str(check))
    if check == 5:
        n = 0
        k = 0
        ang = -0.5
        i = 0
        mode = 3
    if check == 4:
        if binascii.hexlify(response) == 'b0':
            check = 5
        else:
            check = 0
    if check == 3:
        if binascii.hexlify(response) == '02':
            check = 4
        else:
            check = 0
    if check == 2:
        if binascii.hexlify(response) == 'd6':
            check = 3
        else:
            check = 0
    if check == 1:
        if binascii.hexlify(response) == '80':
            check = 2
        else:
            check = 0         
    if check == 0:
        if binascii.hexlify(response) == '02':
            check = 1

while mode == 3: # Collect Data
    response=ser.read()
    if n < 2:
        dataLen[n] = ser.read()
        if n == 1:
            print("dataLen: 0x" + str(binascii.hexlify(dataLen[1]+dataLen[0])))
    else:
        if n < 724:
            rawdata[n-2] = ser.read()
            if n%2 == 0:
                ang += 0.5
            else:
                data_hex[i]= rawdata[n-2]+rawdata[n-3]
                data[i] = int(binascii.hexlify(data_hex[i]),16)
                out[i] = int('{:08b}'.format(data[i]&mask)[::-1],2)
                #out[i] = data[i]&mask

                print(str(i) + ": " + str(out[i]) + " mm, " + str(ang) + " degrees")

                x[i] = out[i]*math.cos(ang*(3.14159/180))
                y[i] = out[i]*math.sin(ang*(3.14159/180))

                i += 1     
        else:
            status = ser.read()
            print("Status: 0x" + str(binascii.hexlify(response)))
            mode = 4
    n +=1

while mode == 4: # Show Data
    ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x25,0x35,0x08])) # Stop continuous data

    plt.plot(x,y)
    plt.show()    
    mode = 5

    
