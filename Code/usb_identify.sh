#!/bin/bash

for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do 
(
    syspath="${sysdevpath%/dev}"
    devname="$(udevadm info -q name -p $syspath)"
	[[ "$devname" == "bus/"* ]] && continue
	string=$(udevadm info -q property --export -p $syspath)
	eval "${string%net.ifnames*}"
    [[ -z "$ID_SERIAL" ]] && continue
	echo "/dev/$devname $ID_SERIAL"
)
done

