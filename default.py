from evdev import ecodes
import time

#user tablet settings
LEFT_HANDED      = False 	#rotate pen and track 180 if true
TRACKPAD_ENABLED = True 	#since it's sort of in the way

# playing with these pressure curves types
PRESSURE_CURVE   = False # LINEAR, SOFT, HARD
#soft = sqrt(z); hard = x^2
#false means no additional calcs, same as LINEAR

FULL_PRESSURE	 = 1.0		# force needed for full pressure, eg 0.8 pen pressure will give a full stroke

# offset of monitor to draw to from top left
# e.g. a dual monitor setup where you're drawing on the right-hand monitor X would be the width of the left monitor 
# for a single monitor setup these are both 0
MONITOR_X = 0
MONITOR_Y = 0

# dimensions of monitor to draw to
MONITOR_W = 1920
MONITOR_H = 1080



def btn1(vbtn): #eyedropper
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.syn()

def btn2(vbtn): #eraser
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 0)
	vbtn.syn()

def btn3(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
	vbtn.syn() 

	#save
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 1)
	# vbtn.syn()

	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 0)
	# vbtn.syn()

def btn4(vbtn): #pen size
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.syn()

def btn5(vbtn): #redo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)
	vbtn.syn()

def btn6(vbtn): #undo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)
	vbtn.syn()


def btn0(vbtn): 
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
	vbtn.syn()

#2 fingers gestures
def gst1(vbtn): # 2 left
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 0)
	vbtn.syn()
def gst2(vbtn): # 2 right
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 0)
	vbtn.syn()
def gst3(vbtn): # 2 up
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_UP, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_UP, 0)
	vbtn.syn()
def gst4(vbtn): # 2 down
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 0)
	vbtn.syn()

#3 fingers gestures
def gst5(vbtn): #left
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTBRACE, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTBRACE, 0)
	vbtn.syn()
def gst6(vbtn): #right
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHTBRACE, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_RIGHTBRACE, 0)
	vbtn.syn()
def gst7(vbtn): #up
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_EQUAL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_EQUAL, 0)
	vbtn.syn()
def gst8(vbtn): #down
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_MINUS, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_MINUS, 0)
	vbtn.syn()

# pinches
def gst9(vbtn): #pinch out/zoom in
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_UP, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_UP, 0)
	vbtn.syn()
def gst10(vbtn): #pinch in/zoom out
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_DOWN, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.BTN_GEAR_DOWN, 0)
	vbtn.syn()



def gst0(vbtn): #any gesture release
	pass