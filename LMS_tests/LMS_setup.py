#!/usr/bin/env python
# Eric Mauro, IGVC 2016
# Last Updated: 2-15-16
import time
import serial
import binascii
import math
import matplotlib.pyplot as plt
import numpy as np

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
                ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
                #config = 1

            elif binascii.hexlify(response[2])=='b1':
                print('LMS291 Connection Status Verified: ' + response[3:10])
                #ser.write(serial.to_bytes([0x02,0x00,0x0A,0x00,0x20,0x00,0x53,0x49,0x43,0x4B,0x5F,0x4C,0x4D,0x53,0xBE,0xC5])) # Settings mode

                ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
                #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180-0.5 degree variant

                #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x64,0x00,0x1D,0x0F])) # 100-1 degree variant
                #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x32,0x00,0xB1,0x59])) # 100-0.5 degree variant
                #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x19,0x00,0xE7,0x72])) # 100-0.25 degree variant

                #config = 1

            elif binascii.hexlify(response[2])=='a0':
                print('LMS291 Installation Mode')
                #ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x20,0x40,0x50,0x08])) # Switch to 38,400 Bd
                #config = 1
            elif binascii.hexlify(response[2])=='bb':
                print('LMS291 Variant Switch')
                if binascii.hexlify(response[3])=='01':
                    print('Switchover successful: ' + str(int(binascii.hexlify(response[4]),16)) + ' by ' + str(int(binascii.hexlify(response[6]),16)/100) + ' degrees')
                    ang_start = (180-int(binascii.hexlify(response[4]),16))/2
                    ang_inc = int(binascii.hexlify(response[6]),16)/100
                    config = 1
                else:
                    print('Switchover failed')
    
while config == 1:
    #ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x36,0x02,0x3E,0x1E])) # Mean Measured Data
    ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
    response=ser.read()
    if binascii.hexlify(response)=='02':
        response=ser.read()
        if binascii.hexlify(response)=='80':
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
            x = [0] * (num+1)		# x and y are the cartesian coordinate of the read data
            y = [0] * (num+1)
            r = [0] * (num+1)		# r and theta are the polar coordinates of the read data
            theta = [0] * (num+1)
			
            for i in range(1, num+1):
                data_low=ser.read()
                data_high=ser.read()
                data[i]=int(binascii.hexlify(data_high+data_low),16)
                print(str(i) + ': ' + str(data[i]) + unit + '@ ' + str(ang) + ' degrees')

                # Save the data in polar form
                r[i] = data[i]
                theta[i] = ang*np.pi/180

                # Save the data in rectangular form
                x[i] = data[i]*math.cos(ang*(np.pi/180))
                y[i] = data[i]*math.sin(ang*(np.pi/180))

                ang += ang_inc

            # Finished data transmission, pick up final message
            status=ser.read()
            print('Status: ' + binascii.hexlify(status))
            response=ser.readline()
            print('Checksum: ' + binascii.hexlify(response))
            time2 = time.time()
            print(str(time2-time1)+' seconds')

			# Show plot
            if n<num_run:
                print(str(theta))
                print(str(r))

                # Polar plot
                ax = plt.subplot(111, projection="polar")
                ax.plot(theta, r, color="r", linewidth=2)
                ax.set_rmax(1000)
                ax.grid(True)
                plt.show()

                # Rectangular plot
                #plt.figure(n)
                #plt.plot(x,y)
                #plt.show(block=False)
                n += 1
            else:
                config = 0
