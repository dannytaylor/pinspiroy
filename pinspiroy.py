# TODO:
# add keybindings to gestures and buttons
# binding for stylus buttons

from evdev import UInput, ecodes, events, AbsInfo, util
import sys
import usb.core
import usb.util
import time

import gst_id
import btn_id
import config

#tablet config values
PEN_MAX_X = 50800
PEN_MAX_Y = 31750 
PEN_MAX_Z = 2048 	#pressure


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
	ecodes.EV_KEY: [ecodes.BTN_TOUCH, ecodes.BTN_LEFT],
	ecodes.EV_ABS: [
		(ecodes.ABS_X, AbsInfo(0,0,PEN_MAX_X,0,0,0)), # same max as pen surface
		(ecodes.ABS_Y, AbsInfo(0,0,PEN_MAX_Y,0,0,0)),],
	}

#button and gesture specs
cap_btn = {
	ecodes.EV_KEY: [ecodes.KEY_A], #don't think we need to specify these, can just inject them as a function
	}

# create our 3 virtual devices
vpen 	= UInput(cap_pen, 	name="pynspiroy-pen", 		version=0x3)
vtrack 	= UInput(cap_track, name="pynspiroy-trackpad", 	version=0x3)
vbtn	= UInput(cap_btn, 	name="pynspiroy-button", 	version=0x3)

time.sleep(0.1) # needed due to some xserver feature 

# input specific functions
def id_btn(data):
	btn_switch[data[4]]()
	
def id_gst(data):
	gst_switch[data[4]]()

def id_trk(data):
	if config.TRACKPAD_ENABLED:
		x = data[3]*255 + data[2]
		y = data[5]*255 + data[4]
		if config.LEFT_HANDED:	
			x = PEN_MAX_X-x
			y = PEN_MAX_Y-y
		vtrack.write(ecodes.EV_ABS, ecodes.ABS_X, x)
		vtrack.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
		vtrack.syn()

#handler for pen input
def id_pen(data):
	x = data[3]*255 + data[2]
	y = data[5]*255 + data[4]
	z = data[7]*255 + data[6]

	#rotate coordinates if left handed
	if config.LEFT_HANDED:
		x = PEN_MAX_X-x
		y = PEN_MAX_Y-y

	#print(str(x) + ', ' + str(y) + '; ' + str(z))
	
	vpen.write(ecodes.EV_MSC,ecodes.MSC_SCAN,50000) # this seems to be necessary, value is arbitrary

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
	1 :btn_id.btn1, #clockwise from top left
	2 :btn_id.btn2, 
	4 :btn_id.btn3, 
	8 :btn_id.btn4, 
	16:btn_id.btn5, 
	32:btn_id.btn6, 

	0 :btn_id.btn0, #button released
}

# switch to handle gesture types
gst_switch = {
	18:gst_id.gst_left, #2 fingers
	19:gst_id.gst_right, 
	20:gst_id.gst_up,
 	21:gst_id.gst_down, 	

 	36:gst_id.gst_left3, #3 fingers
	37:gst_id.gst_right3, 
	34:gst_id.gst_up3,
 	35:gst_id.gst_down3, 

 	22:gst_id.gst_zoomin, #2 fingers expand
 	23:gst_id.gst_zoomout, #2 fingers pinch

 	1 :gst_id.gst_tap1, #single finger tap
 	17:gst_id.gst_tap2, #2 finger tap
 	33:gst_id.gst_tap3, #3 finger tap
 	0 :gst_id.gst_end, #any gesture release

}



# get unidentified huion USB device
# boilerplate USB data reading from pyusb library
dev = usb.core.find(idVendor=0x256c, idProduct=0x006e)
interface = 0
endpoint = dev[0][(0,0)][0]
if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
interface = 1
if dev.is_kernel_driver_active(interface) is True:
	dev.detach_kernel_driver(interface)
	usb.util.claim_interface(dev, interface)
while True:
	try:
		# data received as array of [0,255] ints
		data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
		print (data)
		input_switch[data[1]](data)
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
				continue
usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)

