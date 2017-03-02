import time
from CompassV2 import Compass
from threading import Semaphore

def main():
	c = Compass([], Semaphore(0), Semaphore(0))
	while True:
		print(c.getHeading())
		time.sleep(1)
	
if __name__ == "__main__":
	main()