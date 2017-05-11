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
endpoint1 = dev[0][(0,0)][0]
endpoint2 = dev[0][(1,0)][0]

# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
interface = 0
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

# interface = 2
# if dev.is_kernel_driver_active(interface) is True:
# 	# tell the kernel to detach
# 	dev.detach_kernel_driver(interface)
# 	# claim the device
# 	usb.util.claim_interface(dev, interface)
#bmRequestType, bmRequest, wValue and wIndex
# dev.ctrl_transfer(0x21,0x0a,0x0000,0x01,None)
# dev.write(0x82,None)
# dev.write(0x81,None)

while True:
	try:
		data1 = dev.read(endpoint1.bEndpointAddress,endpoint1.wMaxPacketSize)
		print (data1)
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
				continue
	# try:
	# 	data2 = dev.read(endpoint2.bEndpointAddress,endpoint2.wMaxPacketSize)
	# 	print (data2)
	# except usb.core.USBError as e:
	# 	data = None
	# 	if e.args == ('Operation timed out',):
	# 			continue
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)