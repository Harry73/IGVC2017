import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while 1:
    if (GPIO.input(23)==1):
        print('ON')

    #GPIO.cleanup()
