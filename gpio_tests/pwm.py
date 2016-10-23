# This is not really necessary for our purposes

# Pulsates an LED connected to GPIO pin 1 with a suitable resistor 4 times using softPwm
# softPwm uses a fixed frequency
import wiringpi2 as wpi

MODE = 1 # output mode

PIN = 1

wpi.wiringPiSetup()
wpi.pinMode(PIN, MODE)
wpi.softPwmCreate(PIN, 0, 100) # Setup PWM using Pin, Initial Value and Range parameters
print("PWM setup of pin {0} complete".format(PIN))

wpi.softPwmWrite(PIN, 25) # 25 is the duty cycle, must be between 0 and Range

while True:
	pass
