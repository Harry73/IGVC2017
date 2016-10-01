# Eric Mauro, IGVC 2016
# Last Updated: 2-10 ish

# Analog PWM motor control
# testing oscilloscope average voltage, 1000 Hz PWM
# 25% => 0.89 and 0.9
# 30% => 1.03 amd 1.06
# 40% => 1.49 and 1.51
# 50% => 1.83 and 1.83
# 60% => 2.29 and 2.32
# 70% => 2.74 and 2.75
# 80% => 3.28 and 3.29
# 90% => 3.9 and 3.9
# 95% => 4.27 and 4.27

import RPi.GPIO as GPIO
import time
import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

p1 = GPIO.PWM(18, 1000) # pin 18, 1000 Hz
p2 = GPIO.PWM(12, 1000) # pin 12, 1000 Hz
p1.start(0)
p2.start(0)

screen.addstr(0,0,'Stopped')
dc = 65
p1.ChangeDutyCycle(dc)
p2.ChangeDutyCycle(dc)

try:
    while 1:
        key = screen.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            screen.addstr(0,0,'Forward')
            for m in range(dc,86):
                dc = m
                p1.ChangeDutyCycle(dc)
                p2.ChangeDutyCycle(dc)
                time.sleep(0.05)
        elif key == curses.KEY_DOWN:
            screen.addstr(0,0,'Backward')
            for m in range(dc,54,-1):
                dc = m
                p1.ChangeDutyCycle(dc)
                p2.ChangeDutyCycle(dc)
                time.sleep(0.05)
        elif key == curses.KEY_LEFT:
            screen.addstr(0,0,'LEFT')
            p1.ChangeDutyCycle(85)
            p2.ChangeDutyCycle(55)
        elif key == curses.KEY_RIGHT:
            screen.addstr(0,0,'RIGHT')
            p1.ChangeDutyCycle(55)
            p2.ChangeDutyCycle(85)
        else:
            screen.addstr(0,0,'Stopped')
            dc = 65
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)

except KeyboardInterrupt:
    pass
p1.stop()
p2.stop()
GPIO.cleanup()
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
