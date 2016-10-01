# Eric Mauro
# TCNJ IGVC 2016
# Motor Control program
# Last Updated: 4/4/16

# Notes:
# Does not stop when laser is disconnected
# mm or cm? Just check next time, dummy
# Keep motor controller in microcontroller mode (6 down) to maintain control

import RPi.GPIO as GPIO
import math
import time
import serial
import binascii
import math
import sys
import os

# Establish connection to laser
ser = serial.Serial( 

port='/dev/ttyUSB0',
    baudrate = 38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Setup GPIO Pins
GPIO.setmode(GPIO.BCM) # Use BCM numbers
GPIO.setup(18, GPIO.OUT) # PWM 1
GPIO.setup(12, GPIO.OUT) # PWM 2

p1 = GPIO.PWM(18, 53) # pin 18, 50 Hz
p2 = GPIO.PWM(12, 53) # pin 12, 50 Hz
p1.start(0)
p2.start(0)

# Constants & Variables
dc_plus = 8.5
dc_min = 6.5
dc_stop = 7.5
dc1 = dc_stop # Start in stopped mode
dc2 = dc_stop
m1 = (dc_plus-dc_stop)/2
b1 = (dc_plus+dc_stop)/2
m2 = (dc_min-dc_plus)/2
b2 = (dc_plus+dc_min)/2


R = 1000 # Max vision radius
K = 6 # Turning Gain
way_x = 0
way_y = R

get_data = 0 # Laser data aquisition on/off
count = 0
n = 0

# Stop motor interrupt
def stop():
    p1.ChangeDutyCycle(dc_stop)
    p2.ChangeDutyCycle(dc_stop)
    while 1:
        1 # Must restart program to go again
        
# Main Program
try:
    while 1:
        # PWM to Motors
        p1.ChangeDutyCycle(dc1)
        p2.ChangeDutyCycle(dc2)
        time.sleep(0.1)

        # Laser
        ser.write(serial.to_bytes([0x02,0x00,0x01,0x00,0x31,0x15,0x12])) # Status command
        response = ser.read()
        if binascii.hexlify(response)=='06':
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
                    #get_data = 1
                elif binascii.hexlify(response[2])=='b1':
                    print('LMS291 Connection Status Verified: ' + response[3:10])
                    
                    ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x64,0x00,0x97,0x49])) # 180-1 degree variant
                    #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0xB4,0x00,0x32,0x00,0x3B,0x1F])) # 180-0.5 degree variant
                    
                    #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x64,0x00,0x1D,0x0F])) # 100-1 degree variant
                    #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x32,0x00,0xB1,0x59])) # 100-0.5 degree variant
                    #ser.write(serial.to_bytes([0x02,0x00,0x05,0x00,0x3B,0x64,0x00,0x19,0x00,0xE7,0x72])) # 100-0.25 degree variant
                    
                    #get_data = 1
                elif binascii.hexlify(response[2])=='bb':
                    print('LMS291 Variant Switch')
                    if binascii.hexlify(response[3])=='01':
                        print('Switchover successful: ' + str(int(binascii.hexlify(response[4]),16)) + ' by ' + str(int(binascii.hexlify(response[6]),16)/100.0) + ' degrees')
                        ang_start = (180-int(binascii.hexlify(response[4]),16))/2
                        ang_inc = int(binascii.hexlify(response[6]),16)/100.0
                        get_data = 1
                    else:
                        print('Switchover failed')

        while get_data == 1:
            lasert1=time.time()
            #ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x36,0x02,0x3E,0x1E])) # Mean Measured Data
            ser.write(serial.to_bytes([0x02,0x00,0x02,0x00,0x30,0x01,0x31,0x18])) # Single Scan
            response=ser.read()
            if binascii.hexlify(response)=='02':
                count = 0
                response=ser.read()
                if binascii.hexlify(response)=='80':
                    len_low=ser.read()
                    len_high=ser.read()
                    len = int(binascii.hexlify(len_high+len_low), 16)
                    response=ser.read()
                    #print('Response: ' + binascii.hexlify(response))
                    num_low=ser.read()
                    num_high=ser.read()
                    if int(binascii.hexlify(num_high),16)&int('0x40',16)==0:
                        unit = ' cm '
                    else:
                        unit = ' mm '
                    num=int(binascii.hexlify(num_high+num_low),16)&int('0x3FFF',16)
                    #print('Number of points: ' + str(num))
                
                    ang = ang_start
                    data = [0] * (num+1)
                    #x = [0] * (num+1)
                    #y = [0] * (num+1)
                    Fx = 0
                    Fy = way_y/R
            
                    for i in range(1, num+1):
                        data_low=ser.read()
                        data_high=ser.read()
                        data[i]=int(binascii.hexlify(data_high+data_low),16)
                        #print(str(i) + ': ' + str(data[i]) + unit + '@ ' + str(ang) + ' degrees')
                        #x[i] = data[i]*math.cos(ang*(3.14159/180))
                        #y[i] = data[i]*math.sin(ang*(3.14159/180))
                        if data[i]<R:
                            Fx = Fx-(1-(data[i]/R))*(math.cos(ang*(3.14159/180)))/181
                            Fy = Fy-(1-(data[i]/R))*(math.sin(ang*(3.14159/180)))/181

                        ang += ang_inc
                    status=ser.read()
                    #print('Status: ' + binascii.hexlify(status))
                    response=ser.readline()
                    #print('Checksum: ' + binascii.hexlify(response))

                    lasert2 = time.time()
                    lasert = lasert2-lasert1
                    os.system('clear')
                    print('Data acquired: ' + str(lasert) + ' seconds')
                    #time.sleep(0.1)
                    Fx = K*Fx # Apply Turning Gain
                    if Fx>1:
                        Fx = 1
                    elif Fx<-1:
                        Fx = -1

                    print('Fx = ' + str(Fx))
                    print('Fy = ' + str(Fy))
                    dc1 = m1*Fy+b1 # Forward-backward speed
                    dc2 = m2*Fx+b2 # Left-right speed
                    print('dc1 (FB) = ' + str(dc1))
                    print('dc2 (LR) = ' + str(dc2))
                    p1.ChangeDutyCycle(dc1)
                    p2.ChangeDutyCycle(dc2)
                    
            else:
                count+=1
                if count>5:
                    count = 0
                    get_data = 0

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()
p1.stop()
p2.stop()
GPIO.cleanup()
