from evdev import ecodes
import time
# handlers for gesture actions


def gst_left(vbtn): #2 fingers gestures
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 0)
	vbtn.syn()
def gst_right(vbtn): 
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 0)
	vbtn.syn()
def gst_up(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_UP, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_UP, 0)
	vbtn.syn()
def gst_down(vbtn): 	
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 0)
	vbtn.syn()

#3 fingers gestures
def gst_left3(vbtn): #rotate left
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTBRACE, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTBRACE, 0)
	vbtn.syn()

def gst_right3(vbtn): #rotate right
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHTBRACE, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHTBRACE, 0)
	vbtn.syn()

def gst_up3(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_UP, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_UP, 0)
	vbtn.syn()

def gst_down3(vbtn): 
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_DOWN, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_DOWN, 0)
	vbtn.syn()

def gst_zoomin(vbtn): #2 fingers expand
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_EQUAL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_EQUAL, 0)
	vbtn.syn()
	time.sleep(0.4) #without sleep delay it's kind of hard to control

def gst_zoomout(vbtn): #2 fingers pinch
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_MINUS, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_MINUS, 0)
	vbtn.syn()
	time.sleep(0.4)

def gst_end(vbtn): #any gesture release
	pass