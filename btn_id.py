#handler for button actions
#clockwise from top left
def btn1(): #eyedropper
	KEY_LEFTCTRL 
	pass

def btn2(): #eraser
	KEY_E 
	pass

def btn3(): #pen size
	KEY_LEFTSHIFT
	pass

def btn4(): #undo
	KEY_LEFTCTRL
	KEY_Z
	pass

def btn5(): #redo
	KEY_LEFTCTRL
	KEY_LEFTSHIFT 
	KEY_Z
	pass

def btn6(): #save
	KEY_LEFTCTRL
	KEY_S
	pass

def btn0(): 
	pass
	#vpen.write(ecodes.EV_KEY, ecodes.KEY_A)
