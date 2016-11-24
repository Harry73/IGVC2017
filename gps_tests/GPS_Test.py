import os
from subprocess import Popen, PIPE
from GPS_Consumer import GPS_Consumer
from GPS import GPS
from threading import Thread, Semaphore

os.environ["IGVC_HOME"] = "/home/odroid/IGVC2017"

# Producer-consumer paradigm for the GPS
def main():
	gps_coords_stack = []
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)

	# Get usb device path
	usb_identify_path = os.environ["IGVC_HOME"] + "/gps_tests/usb_identify.sh"
	(stdout, stderr) = Popen([usb_identify_path], stdout=PIPE, stderr=PIPE).communicate()
	if stderr:
		raise Exception(stderr)
	for line in stdout.splitlines():
		pieces = line.split(" ")
		if "Prolific" in pieces[1]:
			gps_device_path = pieces[0]

	# Create Producer and Consumer threads
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s, gps_device_path)
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
