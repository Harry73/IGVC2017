import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

try:
    while 1:
        GPIO.output(16,1)

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
