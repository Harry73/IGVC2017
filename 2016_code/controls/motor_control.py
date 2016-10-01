# Eric Mauro
# TCNJ IGVC 2016
# Motor Control program
# Last Updated: 2/11/16

# Notes:
# Interrupts need timeouts: make counter in while-loop????
# OR one interrupt rising edge for t1 and one interrupt for falling edge for t2
# Should format output with os.system('clear')

import RPi.GPIO as GPIO
import math
import time
import serial
import binascii
import math

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
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Encoder 1
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Encoder 2
GPIO.setup(18, GPIO.OUT) # PWM 1
GPIO.setup(12, GPIO.OUT) # PWM 2

p1 = GPIO.PWM(18, 1000) # pin 18, 1000 Hz
p2 = GPIO.PWM(12, 1000) # pin 12, 1000 Hz
p1.start(0)
p2.start(0)

# Constants & Variables
theta=math.pi/30 # Notch spacing
r = 2.18 # encoder radius, inches
R = 6.5 # wheel radius, inches
dc = 55 # PWM duty cycle (stop, 2.5V)
get_data = 0 # Laser data aquisition on/off
min_d = 2000 # Obstacle distance
count = 0
n = 0
encoder_timeout = 100000

# Stop motor interrupt
def stop():
    dc = 65
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(dc)
    while 1:
        1 # Must restart program to go again
        
# encoder 1 interrupt
def encoder1(channel): 
    start1=time.time()
    while GPIO.input(23) == GPIO.HIGH:
        # Wait until falling edge
        i=1
        #i += 1
        #if i > encoder_timeout:
            #break
    if i < encoder_timeout:
        stop1=time.time()
        t1 = stop1 - start1 # Calculate time between edges
        if t > 0.005: # Filter out impossibly small errors
            w_rads1 = theta/t1
            w_rpm1 = w_rads1*9.5492966
            v_ms1 = R*0.0254*w_rads1
            v_mph1 = v_ms1*2.23694
            print('Motor 1:')
            print(str(w_rpm1)+' RPM')
            print(str(v_mph1)+' MPH')

        time.sleep(0.05)

# encoder 2 interrupt
def encoder2(channel): 
    start2=time.time()
    while GPIO.input(24) == GPIO.HIGH:
        # Wait until falling edge
        i=1
        #i += 1
        #if i > encoder_timeout:
            #break
    if i < encoder_timeout:
        stop2=time.time()
        t2 = stop2 - start2 # Calculate time between edges
        if t > 0.005: # Filter out impossibly small errors
            w_rads2 = theta/t2
            w_rpm2 = w_rads2*9.5492966
            v_ms2 = R*0.0254*w_rads2
            v_mph2 = v_ms2*2.23694
            print('Motor 2:')
            print(str(w_rpm2)+' RPM')
            print(str(v_mph2)+' MPH')

        time.sleep(0.05)

GPIO.add_event_detect(23, GPIO.RISING, callback=encoder1, bouncetime=50)
GPIO.add_event_detect(24, GPIO.RISING, callback=encoder2, bouncetime=50)

# Main Program
try:
    while 1:
        # PWM to Motors
        p1.ChangeDutyCycle(dc)
        p2.ChangeDutyCycle(dc)
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
            
                    for i in range(1, num+1):
                        data_low=ser.read()
                        data_high=ser.read()
                        data[i]=int(binascii.hexlify(data_high+data_low),16)
                        if (i>(110/ang_inc))&(i<(121/ang_inc)):
                            if data[i]<min_d:
                                print('Stop plz')
                                stop()
                        #print(str(i) + ': ' + str(data[i]) + unit + '@ ' + str(ang) + ' degrees')
                        #x[i] = data[i]*math.cos(ang*(3.14159/180))
                        #y[i] = data[i]*math.sin(ang*(3.14159/180))
                        ang += ang_inc
                    status=ser.read()
                    #print('Status: ' + binascii.hexlify(status))
                    response=ser.readline()
                    #print('Checksum: ' + binascii.hexlify(response))

                    lasert2 = time.time()
                    lasert = lasert2-lasert1
                    print('Data acquired: ' + str(lasert) + ' seconds')
                    #time.sleep(0.1)

            else:
                count+=1
                if count>5:
                    count = 0
                    get_data = 0

except KeyboardInterrupt:
    GPIO.cleanup()
p1.stop()
p2.stop()
GPIO.cleanup()
