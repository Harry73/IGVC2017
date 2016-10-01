#!/usr/bin/env python

import time
import serial
import binascii
import math
import matplotlib.pyplot as plt

ser = serial.Serial(

port='/dev/ttyUSB0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# How to Configure
# 1. Power On
# 2. LMS291 Sends "power-on" string
# 3. Send "installation mode" string (20h)
# 4. Acknowledge (06h)
# 5. Response(A0h)
# 6. Set parameters
# 7. Acknowledge (06h)
# 8. Response (F7h)
# 9. Switch to monitoring mode (20h)
# 10. Acknowledge (06h)
# 11. Response (A0h)
# 12. Wait for next request (eg. Start data transmission)

# How to run with default settings
# 1. Power On
# 2. LMS291 Sends "power-on" string
# 3. Send "send data" command
# 4. Acknowledge (06h)
# 5. Response
# 6. Wait for next request (eg. Start data transmission)

config = 0
count = 0
num_run = 1
n = 0

while config==0: 
    response=ser.read()
    if binascii.hexlify(response)=='':
        print('. . .')
        count += 1
    if count == 5:
        ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
        count = 0

    if binascii.hexlify(response)=='06':
        time1 = time.time()
        print('Command Acknowledged')

    if binascii.hexlify(response)=='02':
        response=ser.read()
        if binascii.hexlify(response)=='80':
            response=ser.readline()
            len = int(binascii.hexlify(response[1]+response[0]), 16)
            #print('Length: ' + str(len))
            #print('Response: ' + binascii.hexlify(response[2]))
            #print('Status: ' + binascii.hexlify(response[len+1]))
            #print('Data: ' + binascii.hexlify(response[3:len+1]))

            if binascii.hexlify(response[2])=='90':
                print('LMS291 Powered On')
                #ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
                config = 1
                
            elif binascii.hexlify(response[2])=='b1':
                print('LMS291 Connection Status Verified: ' + response[3:10])
                #ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode
                config = 1
                
            elif binascii.hexlify(response[2])=='a0':
                print('LMS291 Installation Mode')
                #ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x40,0x50,0x08])) # Switch to 38,400 Bd
                #config = 1
            
    
while config == 1:
    ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x36,0x02,0x3E,0x1E])) # Mean Measured Data
    response=ser.read()
    if binascii.hexlify(response)=='02':
        response=ser.read()
        if binascii.hexlify(response)=='80':
            len_low=ser.read()
            len_high=ser.read()
            len = int(binascii.hexlify(len_high+len_low), 16)
            response=ser.read()
            print('Response: ' + binascii.hexlify(response))
            response=ser.read()
            print('Number of scans: ' + str(int(binascii.hexlify(response),16)))
            num_low=ser.read()
            num_high=ser.read()
            if int(binascii.hexlify(num_high),16)&int('0x40',16)==0:
                unit = ' cm '
            else:
                unit = ' mm '
            num=int(binascii.hexlify(num_high+num_low),16)&int('0x3FFF',16)
            print('Number of points: ' + str(num))
                
            ang = 0
            data = [0] * (num+1)
            x = [0] * (num+1)
            y = [0] * (num+1)
            
            for i in range(1, num+1):
                data_low=ser.read()
                data_high=ser.read()
                data[i]=int(binascii.hexlify(data_high+data_low),16)
                print(str(i) + ': ' + str(data[i]) + unit + '@ ' + str(ang) + ' degrees')
                x[i] = data[i]*math.cos(ang*(3.14159/180))
                y[i] = data[i]*math.sin(ang*(3.14159/180))
                ang += 0.5
            status=ser.read()
            print('Status: ' + binascii.hexlify(status))
            response=ser.readline()
            print('Checksum: ' + binascii.hexlify(response))
            time2 = time.time()
            print(str(time2-time1)+' seconds')

            if n<num_run:
                plt.figure(n)
                plt.plot(x,y)
                plt.show(block=False)
                n += 1
            else:
                config = 0
