import wiringpi2
PIN_TO_SENSE = 2

count = 0

def gpio_callback():
    global count
    count += 1
    print(count)
    print("GPIO_CALLBACK!")

wiringpi2.wiringPiSetup()
wiringpi2.pinMode(PIN_TO_SENSE, wiringpi2.GPIO.INPUT)
wiringpi2.wiringPiISR(PIN_TO_SENSE, wiringpi2.GPIO.INT_EDGE_FALLING, gpio_callback)

while True:
    wiringpi2.delay(2000)
