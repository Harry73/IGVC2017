# Uses a pygame interface to control the motors manually

# CHECK IF wpi.delayMicroseconds is a blocking function. I think it is, but it's a problem if it is not.

import sys
import time
import pygame
from pygame.locals import *
from Motors import Motors

# Define colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 199, 206)
YELLOW = (255, 235, 156)
GREEN  = (198, 239, 206)

def main():
	global WINDOW, FONT, drivePin, turnPin, motors

	# pygame setup
	pygame.init()
	FONT = pygame.font.SysFont("Calibri", 15)
	WINDOW = pygame.display.set_mode((500, 500))
	pygame.display.set_caption('Manual Drive')

	# Motors setup
	motors = Motors()
	motors.start()

	run()

def run():
	start = False
	value1 = "hi"
	value2 = "hi"

	# First time draw
	WINDOW.fill(GREEN)
	pygame.draw.rect(WINDOW, YELLOW, (0, 200, 500, 100))
	pygame.draw.rect(WINDOW, YELLOW, (200, 0, 100, 500))
	pygame.draw.rect(WINDOW, RED, (200, 200, 100, 100))
	label = FONT.render("{0}, {1}".format(value1, value2), 1, BLACK)
	WINDOW.blit(label, (400, 10))
	pygame.display.update()

	# Main "game" loop
	while True:
		# Handle events
		for event in pygame.event.get():
			# Quit conditions
			if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
				motors.terminate()
				pygame.quit()
				sys.exit()

			# Draw a background guide
			elif event.type == MOUSEBUTTONDOWN:
				mouseX, mouseY = event.pos
				if start:
					if mouseY >= 200 and mouseY <= 300:		# stop
						motors.drive(1360)
						value1 = "stop"
					elif mouseY < 200:						# forward
						pulse = int(8/5*mouseY+1000)
						motors.drive(pulse)
						value1 = str(pulse)
					elif mouseY > 300:						# backward
						pulse = int(8/5*mouseY+920)
						motors.drive(pulse)
						value1 = str(pulse)

					if mouseX >= 200 and mouseX <= 300:		# no turn
						motors.turn(1000)
						value2 = "no turn"
					elif mouseX < 200:						# left
						pulse = int(-5/2*mouseX+1500)
						motors.turn(pulse)
						value2 = str(pulse)
					elif mouseX > 300:						# right
						pulse = int(-5/2*mouseX+1750)
						motors.turn(pulse)
						value2 = str(pulse)

					# Redraw window
					WINDOW.fill(GREEN)
					pygame.draw.rect(WINDOW, YELLOW, (0, 200, 500, 100))
					pygame.draw.rect(WINDOW, YELLOW, (200, 0, 100, 500))
					pygame.draw.rect(WINDOW, RED, (200, 200, 100, 100))
					label = FONT.render("{0}, {1}".format(value1, value2), 1, BLACK)
					WINDOW.blit(label, (400, 10))
					pygame.display.update()

			# Toggle starting and stopping the control
			elif event.type == KEYDOWN and event.key == K_RETURN:
				if start:
					motors.stop()
					start = False
				else:
					motors.restart()
					start = True

				# Redraw window
				WINDOW.fill(GREEN)
				pygame.draw.rect(WINDOW, YELLOW, (0, 200, 500, 100))
				pygame.draw.rect(WINDOW, YELLOW, (200, 0, 100, 500))
				pygame.draw.rect(WINDOW, RED, (200, 200, 100, 100))
				label = FONT.render("{0}, {1}".format(value1, value2), 1, BLACK)
				WINDOW.blit(label, (400, 10))
				pygame.display.update()
		
		time.sleep(0.1)

if __name__ == "__main__":
	main()
