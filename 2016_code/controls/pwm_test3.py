# Eric Mauro, IGVC 2016
# Last Updated: 2-15-16

# R/C Mode Motor Control
# Notes:
#   (50Hz) at -100% and +60%, wheels move at about the same speed but in opposite directions
#   frequency changed from 50 Hz to about 53 Hz to cancel out slight delay and duty cycle error in PWM signal


import RPi.GPIO as GPIO
import time
import curses

screen = curses.initscr()
screen.border(0)
screen.refresh()
curses.noecho()
curses.cbreak()
screen.keypad(True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

p1 = GPIO.PWM(18, 53) # pin 18, 50 Hz
p2 = GPIO.PWM(12, 53) # pin 12, 50 Hz
p1.start(0)
p2.start(0)

mixed = 1 # Mixed or independent mode
          # Independent: p1 = left motor, p2 = right motor
          # Mixed: p1 = forward/backward, p2 = left/right

dc_plus = 9 # Start in slow mode
dc_min = 6
dc_stop = 7.5

screen.addstr(12,35,'STOP')
dc = dc_stop # Start in stopped state
p1.ChangeDutyCycle(dc)
p2.ChangeDutyCycle(dc)
screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')

try:
    while 1:
        key = screen.getch()
        if key == ord('q'):
            break
        elif key == ord('1'):
            screen.addstr(10,35,'SLOW MODE')
            dc_plus = 9
            dc_min = 6
        elif key == ord('2'):
            screen.addstr(10,35,'FAST MODE')
            dc_plus = 10
            dc_min = 5
        elif key == curses.KEY_UP:
            screen.clear()
            screen.border(0)
            screen.addstr(12,35,'FORWARD')
            if mixed == 0:
                dc = dc_plus
                p1.ChangeDutyCycle(dc)
                screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
                p2.ChangeDutyCycle(dc+1.5)
                screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')
            else:
                dc = dc_plus
                p1.ChangeDutyCycle(dc)
                dc = dc_stop
                p2.ChangeDutyCycle(dc)
                
        elif key == curses.KEY_DOWN:
            screen.clear()
            screen.border(0)
            screen.addstr(12,35,'BACKWARD')
            if mixed == 0:
                dc = dc_min
                p1.ChangeDutyCycle(dc)
                screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
                p2.ChangeDutyCycle(dc)
                screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')
            else:
                dc = dc_min
                p1.ChangeDutyCycle(dc)
                dc = dc_stop
                p2.ChangeDutyCycle(dc)
                
        elif key == curses.KEY_LEFT:
            screen.clear()
            screen.border(0)
            screen.addstr(12,35,'LEFT')
            if mixed == 0:
                dc = dc_min
                p1.ChangeDutyCycle(dc)
                screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
                dc = dc_plus
                p2.ChangeDutyCycle(dc)
                screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')
            else:
                dc = dc_stop
                p1.ChangeDutyCycle(dc)
                dc = dc_plus 
                p2.ChangeDutyCycle(dc)
                
        elif key == curses.KEY_RIGHT:
            screen.clear()
            screen.border(0)
            screen.addstr(12,35,'RIGHT')
            if mixed == 0:
                dc = dc_plus
                p1.ChangeDutyCycle(dc)
                screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
                dc = dc_min
                p2.ChangeDutyCycle(dc)
                screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')
            else:
                dc = dc_stop
                p1.ChangeDutyCycle(dc)
                dc = dc_min 
                p2.ChangeDutyCycle(dc)
        else:
            screen.clear()
            screen.border(0)
            screen.addstr(12,35,'STOP')
            dc = dc_stop
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
            screen.addstr(15,20, 'LW: '+str(40.0*dc-300)+'%')
            screen.addstr(15,50, 'RW: '+str(40.0*dc-300)+'%')

except KeyboardInterrupt:
    pass
p1.stop()
p2.stop()
GPIO.cleanup()
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
