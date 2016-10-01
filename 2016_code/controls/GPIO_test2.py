import RPi.GPIO as GPIO
import math
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
theta=math.pi/30
r = 2.18 # encoder radius, inches
R = 6.5 # wheel radius, inches

def encoder(channel):
    start=time.time()
    while GPIO.input(23) == GPIO.HIGH:
        1
    stop=time.time()
    t = stop - start
    if t > 0.005:
        w_rads = theta/t
        w_rpm = w_rads*9.5492966
        v_ms = R*0.0254*w_rads
        v_mph = v_ms*2.23694
        print(str(w_rpm)+' RPM')
        print(str(v_mph)+' MPH')

    time.sleep(0.05)

GPIO.add_event_detect(23, GPIO.RISING, callback=encoder, bouncetime=50)

i = 0
try:
    while 1:
        i+=1 # Dummy Program
        if i == 50000:
            #print('Not yet')
            i = 0
            
            
    
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
