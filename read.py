#!/usr/bin/python

# Simple USB reading to console
# adapted from https://www.orangecoat.com/how-to/read-and-decode-data-from-your-mouse-using-this-pyusb-hack
# using pyusb

import sys
import usb.core
import usb.util
import time

#decimal vendor and product values
dev = usb.core.find(idVendor=0x256c, idProduct=0x006e)
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
	# tell the kernel to detach
	dev.detach_kernel_driver(interface)
	# claim the device
	usb.util.claim_interface(dev, interface)

interface = 1
if dev.is_kernel_driver_active(interface) is True:
	# tell the kernel to detach
	dev.detach_kernel_driver(interface)
	# claim the device
	usb.util.claim_interface(dev, interface)

while True:
	try:
		data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
		print (data)
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
				continue
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)