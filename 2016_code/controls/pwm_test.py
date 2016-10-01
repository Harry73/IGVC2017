import time
import sys
import os

#stop
os.system('echo "17=0.65">/dev/pi-blaster')
os.system('echo "18=0.65">/dev/pi-blaster')
time.sleep(2)

#forward
os.system('echo "17=0.7">/dev/pi-blaster')
os.system('echo "18=0.65">/dev/pi-blaster')
time.sleep(2)

#reverse
os.system('echo "17=0.55">/dev/pi-blaster')
os.system('echo "18=0.65">/dev/pi-blaster')
time.sleep(2)


#right
os.system('echo "17=0.65">/dev/pi-blaster')
os.system('echo "18=0.7">/dev/pi-blaster')
time.sleep(2)

#left
os.system('echo "17=0.65">/dev/pi-blaster')
os.system('echo "18=0.55">/dev/pi-blaster')
time.sleep(2)

#stop
os.system('echo "17=0.65">/dev/pi-blaster')
os.system('echo "18=0.65">/dev/pi-blaster')
