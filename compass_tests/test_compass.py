import time
from Compass import Compass

def main():
	c = Compass()
	while True:
		bearing = c.orientation()
		print(bearing)
		time.sleep(1)
	
if __name__ == "__main__":
	main()