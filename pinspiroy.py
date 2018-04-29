#!/usr/bin/python

from evdev import UInput, ecodes, events, AbsInfo, util
import sys
import usb.core
import usb.util
import time
import gtk

import bindings
import math
import config as g

#tablet config values
PEN_MAX_X = 50800
PEN_MAX_Y = 31750 
PEN_MAX_Z = 2048 	#pressure

# user specs
MAX_W = gtk.gdk.screen_width()
MAX_H = gtk.gdk.screen_height()

x_scale  = g.MONITOR_W/float(MAX_W)
x_offset = PEN_MAX_X*g.MONITOR_X/float(MAX_W)
y_scale  = g.MONITOR_H/float(MAX_H)
y_offset = PEN_MAX_Y*g.MONITOR_Y/float(MAX_H)

msc = 1
#specify capabilities for a virtual device
#one for each device:
#pen/pad, trackpad, and buttons
#note: I've chosen to include trackpad gestures with the buttons based on how they're reported over USB

#pressure sensitive pen tablet area with 2 stylus buttons and no eraser
cap_pen = {
	ecodes.EV_KEY: [ecodes.BTN_TOUCH, ecodes.BTN_TOOL_PEN],
	ecodes.EV_ABS: [
		(ecodes.ABS_X, AbsInfo(0,0,PEN_MAX_X,0,0,5080)), #value, min, max, fuzz, flat, resolution
		(ecodes.ABS_Y, AbsInfo(0,0,PEN_MAX_Y,0,0,5080)),
		(ecodes.ABS_PRESSURE, AbsInfo(0,0,PEN_MAX_Z,0,0,0)),],
	ecodes.EV_MSC: [ecodes.MSC_SCAN], #not sure why, but it appears to be needed
	}

#trackpad specs
cap_track = {
	ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE],
	ecodes.EV_ABS: [
		(ecodes.ABS_X, AbsInfo(0,0,PEN_MAX_X,0,0,0)), # same max as pen surface
		(ecodes.ABS_Y, AbsInfo(0,0,31620,0,0,0)),],
	}

#buttons must be defined in the same sequential order as in the Linux specs
#https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
cap_btn = {
	ecodes.EV_KEY: [ecodes.KEY_MINUS,ecodes.KEY_EQUAL,ecodes.KEY_E, 
					ecodes.KEY_LEFTBRACE,ecodes.KEY_RIGHTBRACE,
					ecodes.KEY_LEFTCTRL, ecodes.KEY_S, ecodes.KEY_LEFTSHIFT, ecodes.KEY_Z,
					ecodes.KEY_LEFTALT, ecodes.KEY_SPACE,
					ecodes.KEY_UP, ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_DOWN, 
					ecodes.BTN_MOUSE, ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE]
	}

# create our 3 virtual devices
vpen 	= UInput(cap_pen, 	name="pinspiroy-pen", 		version=0x3)
vtrack 	= UInput(cap_track, name="pinspiroy-trackpad", 	version=0x4)
vbtn	= UInput(cap_btn, 	name="pinspiroy-button", 	version=0x5)

time.sleep(0.1) # needed due to some xserver feature 

# input specific functions
def id_btn(data):
	if g.LEFT_HANDED:
		btn_switch_LH[data[4]](vbtn)
	else:
		btn_switch[data[4]](vbtn)
	
def id_gst(data):
	if data[4] == 24 or data[4] == 25:
		print('key error: ' + str(data[4]))
	elif g.LEFT_HANDED:
		gst_switch_LH[data[4]](vbtn)
	else:
		gst_switch[data[4]](vbtn)

def id_trk(data):
	if g.TRACKPAD_ENABLED:
		x = data[3]*256 + data[2]
		y = data[5]*256 + data[4]
		if g.LEFT_HANDED:	
			x = PEN_MAX_X-x
			y = PEN_MAX_Y-y
		x = int(math.floor(x*x_scale+x_offset))
		y = int(math.floor(y*y_scale+y_offset))
		vtrack.write(ecodes.EV_ABS, ecodes.ABS_X, x)
		vtrack.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
		vtrack.syn()

def pressure_curve(z):
	z = z/g.FULL_PRESSURE
	if z > PEN_MAX_Z:
		z = PEN_MAX_Z
	if g.PRESSURE_CURVE == 'LINEAR':
		pass
	elif g.PRESSURE_CURVE == 'HARD':
		z = z*z/PEN_MAX_Z
	elif g.PRESSURE_CURVE == 'SOFT':
		z = z*math.sqrt(z)/math.sqrt(PEN_MAX_Z)
	return math.floor(z)

#handler for pen input
def id_pen(data):
	x = data[3]*256 + data[2]
	y = data[5]*256 + data[4]
	z = data[7]*256 + data[6]
	
	if g.PRESSURE_CURVE:
		z = pressure_curve(z)
	#rotate coordinates if left handed
	if g.LEFT_HANDED:
		x = PEN_MAX_X-x
		y = PEN_MAX_Y-y

	x = int(math.floor(x*x_scale+x_offset))
	y = int(math.floor(y*y_scale+y_offset))

	vpen.write(ecodes.EV_ABS, ecodes.ABS_X, x)
	vpen.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
	vpen.write(ecodes.EV_ABS, ecodes.ABS_PRESSURE, z)

	if data[1] == 128: # pen registered, but not touching pad
		vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 0)
	elif data[1] == 130: # stylus button 1
		if z>10:
			vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 1)
		else:
			vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 0)
		vpen.write(ecodes.EV_KEY, ecodes.BTN_STYLUS, 1)
	elif data[1] == 132: # stylus button 2
		if z>10:
			vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 1)
		else:
			vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 0)
		vpen.write(ecodes.EV_KEY, ecodes.BTN_STYLUS2, 1)
	elif data[1] == 129: # == 129; pen touching pad
		vpen.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, 1)

	vpen.write(ecodes.EV_KEY, ecodes.BTN_TOOL_PEN, 1)

	vpen.syn() #sync all inputs together

def gst_tap1(whatever): #single finger tap
	if g.TRACKPAD_ENABLED:
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
		vtrack.syn()
def gst_tap2(whatever): #single finger tap
	if g.TRACKPAD_ENABLED:
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 1)
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 0)
		vtrack.syn()
def gst_tap3(whatever): #single finger tap
	if g.TRACKPAD_ENABLED:
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_MIDDLE, 1)
		vtrack.write(ecodes.EV_KEY, ecodes.BTN_MIDDLE, 0)
		vtrack.syn()

# switch to handle input types
input_switch = {
	224:id_btn, #buttonpad 
	225:id_gst, #trackpad gestures
	144:id_trk, #trackpad movement
	129:id_pen, #stylus down
	128:id_pen, #stylus up
	130:id_pen, #stylus button 1
	132:id_pen,	#stylus button 2
}

# switch to handle button types
btn_switch = {
	1 :bindings.btn1, #clockwise from top left
	2 :bindings.btn2, 
	4 :bindings.btn3, 
	8 :bindings.btn4, 
	16:bindings.btn5, 
	32:bindings.btn6, 

	0 :bindings.btn0, #button released
}

# reverse button order for LH setting
btn_switch_LH = {
	32:bindings.btn1, #clockwise from top left
	16:bindings.btn2, 
	8 :bindings.btn3, 
	4 :bindings.btn4, 
	2 :bindings.btn5, 
	1 :bindings.btn6, 

	0 :bindings.btn0, #button released
}

# switch to handle gesture types
gst_switch = {
	18:bindings.gst_left, #2 fingers
	19:bindings.gst_right, 
	20:bindings.gst_up,
 	21:bindings.gst_down, 	

 	36:bindings.gst_left3, #3 fingers
	37:bindings.gst_right3, 
	34:bindings.gst_up3,
 	35:bindings.gst_down3, 

 	22:bindings.gst_zoomin, #2 fingers expand
 	23:bindings.gst_zoomout, #2 fingers pinch

 	1 :gst_tap1, #single finger tap
 	17:gst_tap2, #2 finger tap
 	33:gst_tap3, #3 finger tap
 	0 :bindings.gst_end, #any gesture release

}
#reverse gesture axes for LH setting
gst_switch_LH = {
	19:bindings.gst_left, #2 fingers
	18:bindings.gst_right, 
	21:bindings.gst_up,
 	20:bindings.gst_down, 	

 	37:bindings.gst_left3, #3 fingers
	36:bindings.gst_right3, 
	35:bindings.gst_up3,
 	34:bindings.gst_down3, 

 	22:bindings.gst_zoomin, #2 fingers expand
 	23:bindings.gst_zoomout, #2 fingers pinch

 	1 :gst_tap1, #single finger tap
 	17:gst_tap2, #2 finger tap
 	33:gst_tap3, #3 finger tap
 	0 :bindings.gst_end, #any gesture release

}



# get unidentified huion USB device
# boilerplate USB data reading from pyusb library
dev = usb.core.find(idVendor=0x256c, idProduct=0x006e)
interface = 0
endpoint = dev[0][(0,0)][0]

try:
	usb.util.get_string(dev, 0xc8, 1033)
	print('Graphics tablet enabled.')
except:
	print('')

if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
	print('interface 0 grabbed')
interface = 1
if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
	print('interface 1 grabbed')

print('pinspiroy driver should be running!')
while True:
	try:
		# data received as array of [0,255] ints
		data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
		input_switch[data[1]](data)
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
				continue
usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)
