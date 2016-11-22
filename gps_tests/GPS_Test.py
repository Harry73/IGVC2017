from GPS_Consumer import GPS_Consumer
from GPS import GPS
from threading import Thread, Semaphore

# Producer-consumer paradigm for the GPS
def main():
	gps_coords_stack = []
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	
	# Create Producer and Consumer threads
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s)
	gps_printer = GPS_Consumer(gps_coords_stack, gps_n, gps_s)
	
	# Start all the threads
	gps_sensor.start()
	gps_printer.start()
	
	# Wait for threads to finish
	gps_sensor.join()
	gps_printer.join()
	
	print("Done.")
	print(gps_coords_stack)

if __name__ == "__main__":
	main()
