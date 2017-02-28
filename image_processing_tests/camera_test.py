import time
from Camera import Camera
from threading import Thread, Semaphore

def main():
	# Camera setup
	camera_stack = []
	camera_n = Semaphore(0)
	camera_s = Semaphore(1)
	cameras = Camera(camera_stack, camera_n, camera_s)

	# Start the thread
	cameras.start()
	
	# Try to pull from the stack every 1 second and print data
	for i in range(0, 10):
		time.sleep(1)
		camera_n.acquire()
		camera_s.acquire()
		left_lines = camera_stack.pop()
		right_lines = camera_stack.pop()
		camera_s.release()
		
		print(i)
		if right_lines != None:
			for line in right_lines:
				for rho, theta in line:
					print(rho, theta)
		else:
			print("No right lines")
			
		if left_lines != None:
			for line in left_lines:
				for rho, theta in line:
					print(rho, theta)
		else:
			print("No left lines")
	
	# Stop camera thread and wait for it to finish
	cameras.stop()
	cameras.join()
	
if __name__ == "__main__":
	main()