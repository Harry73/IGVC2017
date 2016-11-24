from subprocess import Popen, PIPE
from GPS import GPS
from threading import Thread, Semaphore

IGVC_HOME = "/home/odroid/IGVC2017"

def main():
	device_to_path = get_device_paths()

	# GPS setup
	gps_coords_stack = []
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s, device_to_path["GPS"])
	
	# Start all the threads
	gps_sensor.start()
	
def get_device_paths():
	# Get usb device paths
	usb_identify_path = IGVC_HOME + "/gps_tests/usb_identify.sh"
	(stdout, stderr) = Popen([usb_identify_path], stdout=PIPE, stderr=PIPE).communicate()
	
	if stderr:
		raise Exception(stderr)

	# Create dictionary of device to path
	device_to_path = {}
		
	for line in stdout.splitlines():
		pieces = line.split(" ")
		if "Prolific" in pieces[1]:
			device_to_path["GPS"] = pieces[0]

	return device_to_path
	
if __name__ == "__main__":
	main()
