"""
Motors
"""
import wiringpi2 as wpi
from threading import Thread

class Motors:
		
	angle = 0
	countTurns = 0
	countSteps = 0

	#initialization of pins
	def __init__(self):
		wpi.wiringPiSetup()
		pins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23,26,27,30,31]
		#GPIO pin setup
		for x in pins:
			wpi.pinMode(x,1)
			wpi.digitalWrite(x,0)
		#initialize threads
		TurnCounter = Thread(target=PhotoIntA.startCount())

	def run(self):
	def move(self):

#this does not work, no way of going backwards
	def turn(turnangle,self):
		countTurns = 0 #keep
		angle = Compass.getAngle() #keep
		goal = angle + turnangle #keep
		if turnangle < 0 #keep
			turnspeed = 1300 #keep
		else #keep
			turnspeed = 1500 #keep
		#Start Turning
		TurnCounter.start()#PhotoInterrupter Counter
		wpi.digitalWrite(1,1)#S1
		wpi.delayMicroseconds(turnspeed)
		wpi.digitalWrite(1,0)
		#Turn robot until angle reaches goal to 10% error
		while True:
			if angle >= (0.95)*goal and angle <= (1.05)*goal
				countTurns = PhotoIntA.getCount()
				reset()
				break
			#overshoot checking
			if angle > goal and turnangle > 0
				#change direction
				wpi.digitalWrite(1,1)#S1
				wpi.delayMicroseconds(turnspeed-200)
				wpi.digitalWrite(1,0)
			if angle < goal and turnangle < 0
				#change direction
				wpi.digitalWrite(1,1)#S1
				wpi.delayMicroseconds(turnspeed+200)
				wpi.digitalWrite(1,0)
			angle = Compass.getAngle()

	#reset turning axle to original place		
	def reset(self):
			
	#soft stop for all motors	
	def stop(self):
		wpi.digitalWrite(1,1)#S1
		wpi.digitalWrite(2,1)#S2
		wpi.delayMicroseconds(1400)#stop pulse width
		wpi.digitalWrite(1,0)
		wpi.digitalWrite(2,0)
