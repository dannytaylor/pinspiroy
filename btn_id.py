from evdev import ecodes

#handler for button actions
#clockwise from top left



def btn1(vbtn): #eyedropper
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.syn()

def btn2(vbtn): #eraser
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_E, 0)
	vbtn.syn()

def btn3(vbtn): #pen size
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.syn()

def btn4(vbtn): #undo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)
	vbtn.syn()

def btn5(vbtn): #redo
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 1)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_Z, 0)
	vbtn.syn()

def btn6(vbtn):
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
	vbtn.syn() 

	#save
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 1)
	# vbtn.syn()

	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	# vbtn.write(ecodes.EV_KEY, ecodes.KEY_S, 0)
	# vbtn.syn()

def btn0(vbtn): 
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
	vbtn.syn()