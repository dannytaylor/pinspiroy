#pinwiz2.py
import gtk

class PinWiz(gtk.Window):
	p = [1,2,3,4]
	v = [0,0,0,0]
	v[0] = [0,0,1,2,2,3,3] # track, left, pressure, ox, oy, dx, dy
	v[1] = [1,2,3,4,5,6] # btn 1-6
	v[2] = [1,2,3,4,5,6,7,8] # direction gestures, 2/3 l,r,u,d
	v[3] = [1,1,2,2,2] #pinch in/out, tap 1/2/3
	n = [1,2,3,4] #next buttons

	def __init__(self):
		super(PinWiz, self).__init__()
		self.set_title("pin wiz config tool")
		self.set_size_request(320, 480)
		self.set_border_width(8)
		self.set_position(gtk.WIN_POS_CENTER)

		main = gtk.VBox(False, 5)

		for i in range(0,3):
			self.p[i] = gtk.VBox(False,5)

		# bottom of window  buttons
		bottom_bar = gtk.HBox(True, 3)
		cancel = gtk.Button("cancel")
		cancel.set_size_request(70, 30)
		cancel.connect("clicked",self.quit)
		bottom_bar.add(cancel)
		for i in range(0,3):
			self.n[i] = gtk.Button("next")
			#self.n[i].connect("clicked",self.cont(i))
			bottom_bar.add(self.n[i])

		halign = gtk.Alignment(1, 0, 0, 0)
		halign.add(bottom_bar)

		for i in range(0,3):
			main.pack_start(self.p[i], False, False, 8)

		for i in range(0,4):
			for j in range(0,len(self.v[i])):
				self.v[i][j] = gtk.Label("test")



		self.show_all()
		for i in range(1,3):
			self.p[i].hide()
			self.n[i].hide()


	def quit(self,widget,data=None):
		gtk.main_quit()

PinWiz()
gtk.main()

def mk_widget(type):
	btn= gtk.combo_box_new_text()
	if type == "mod":
		btn.set_size_request(24,24)
		btn.append_text('')
		btn.append_text('KEY_LEFTCTRL')
		btn.append_text('KEY_LEFTALT')
		btn.append_text('KEY_LEFTSHIFT')
		btn.set_active(0)
		btn = gtk.combo_box_new_text()
		return btn
	else:
		for key in keys:
			btn.append_text(keys[key])
		return btn

keys = [
	'KEY_ESC',
	'KEY_1',
	'KEY_2',
	'KEY_3',
	'KEY_4',
	'KEY_5',
	'KEY_6',
	'KEY_7',
	'KEY_8',
	'KEY_9',
	'KEY_0',
	'KEY_MINUS',
	'KEY_EQUAL',
	'KEY_BACKSPACE',
	'KEY_TAB',
	'KEY_Q',
	'KEY_W',
	'KEY_E',
	'KEY_R',
	'KEY_T',
	'KEY_Y',
	'KEY_U',
	'KEY_I',
	'KEY_O',
	'KEY_P',
	'KEY_LEFTBRACE',
	'KEY_RIGHTBRACE',
	'KEY_ENTER',
	'KEY_A',
	'KEY_S',
	'KEY_D',
	'KEY_F',
	'KEY_G',
	'KEY_H',
	'KEY_J',
	'KEY_K',
	'KEY_L',
	'KEY_SEMICOLON',
	'KEY_APOSTROPHE',
	'KEY_GRAVE',
	'KEY_LEFTSHIFT',
	'KEY_BACKSLASH',
	'KEY_Z',
	'KEY_X',
	'KEY_C',
	'KEY_V',
	'KEY_B',
	'KEY_N',
	'KEY_M',
	'KEY_COMMA',
	'KEY_DOT',
	'KEY_SLASH',
	'KEY_LEFTALT',
	'KEY_SPACE',
	'KEY_F1',
	'KEY_F2',
	'KEY_F3',
	'KEY_F4',
	'KEY_F5',
	'KEY_F6',
	'KEY_F7',
	'KEY_F8',
	'KEY_F9',
	'KEY_F10',
	'KEY_KP7',
	'KEY_KP8',
	'KEY_KP9',
	'KEY_KP4',
	'KEY_KP5',
	'KEY_KP6',
	'KEY_KP1',
	'KEY_KP2',
	'KEY_KP3',
	'KEY_KP0',
	'KEY_UP',
	'KEY_PAGEUP',
	'KEY_LEFT',
	'KEY_RIGHT',
	'KEY_END',
	'KEY_DOWN',
	'KEY_PAGEDOWN',
	'KEY_INSERT',
	'KEY_DELETE'
]