# Min: 864
# Max: 1857
# Off range: 1320 - 1400

# CHECK IF wpi.delayMicroseconds is a blocking function. I think it is, but it's a problem if it is not. 

import sys
import pygame
import wiringpi2 as wpi
from pygame.locals import *

# Define colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 199, 206)
YELLOW = (255, 235, 156)
GREEN  = (198, 239, 206)

def main():
	global WINDOW, FONT, drivePin, turnPin

	# Setup
	wpi.wiringPiSetup()
	drivePin = 1
	turnPin = 2
	wpi.pinMode(drivePin, 1)
	wpi.digitalWrite(drivePin, 0)
	wpi.pinMode(turnPin, 1)
	wpi.digitalWrite(turnPin, 0)
	
	pygame.init()
	FONT = pygame.font.SysFont("Calibri", 15)
	WINDOW = pygame.display.set_mode((500, 500))
	pygame.display.set_caption('Manual Drive')

	run()

def run():
	start = False

	# Main "game" loop
	while True:
		# Handle events
		for event in pygame.event.get():
			# Quit conditions
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

			# Draw a background guide
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos

				WINDOW.fill(GREEN)
				pygame.draw.rect(WINDOW, YELLOW, (0, 200, 500, 100))
				pygame.draw.rect(WINDOW, YELLOW, (200, 0, 100, 500))
				pygame.draw.rect(WINDOW, RED, (200, 200, 100, 100))

				label = FONT.render("{0}, {1}".format(mousex, mousey), 1, BLACK)
				WINDOW.blit(label, (400, 10))

			elif event.type == KEYDOWN and event.key == K_RETURN:
				start = True

		# Redraw window
		pygame.display.update()

		# Handle vehicle control
		if start:
			if mousey >= 200 and mousey <= 300:		# stop
				wpi.digitalWrite(drivePin, 1)
				wpi.delayMicroseconds(1360)
				wpi.digitalWrite(drivePin, 0)
			elif mousey < 200:						# forward
				wpi.digitalWrite(drivePin, 1)
				wpi.delayMicroseconds(-457/200.0*mousey+1857.0)
				wpi.digitalWrite(drivePin, 0)
			elif mousey > 300:						# backward
				wpi.digitalWrite(drivePin, 1)
				wpi.delayMicroseconds(-57/25.0*mousey+2004.0)
				wpi.digitalWrite(drivePin, 0)
				
			if mousex >= 200 and mousex <= 300:		# no turn
				wpi.digitalWrite(turnPin, 1)
				wpi.delayMicroseconds(1360)
				wpi.digitalWrite(turnPin, 0)
			elif mousex < 200:						# left
				wpi.digitalWrite(turnPin, 1)
				wpi.delayMicroseconds(57/25.0*mousex+864)
				wpi.digitalWrite(turnPin, 0)
			elif mousex > 300:						# right
				wpi.digitalWrite(turnPin, 1)
				wpi.delayMicroseconds(457/200.0*mousex+1429/2.0)
				wpi.digitalWrite(turnPin, 0)

if __name__ == "__main__":
	main()
	