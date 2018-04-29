#!/usr/bin/python

import gtk

class PinWiz(gtk.Window):
	page1,page2,page3,page4,next1,next2,next3,export=0,0,0,0,0,0,0,0

	def __init__(self):
		super(PinWiz, self).__init__()

		self.set_title("pin wiz config tool")
		self.set_size_request(360, 520)
		self.set_border_width(8)
		self.set_position(gtk.WIN_POS_CENTER)

		vbox = gtk.VBox(False, 5)
		self.page1 = gtk.VBox(False, 5)
		self.page2 = gtk.VBox(False, 5)
		self.page3 = gtk.VBox(False, 5)
		self.page4 = gtk.VBox(False, 5)

		align_bottom = gtk.Alignment(0, 1, 0, 0)
		align_top = gtk.Alignment(0, 0, 0, 0)
		
		# bottom of window  buttons
		hbox = gtk.HBox(True, 3)
		cancel = gtk.Button("cancel")
		cancel.set_size_request(70, 30)
		cancel.connect("clicked",self.quit)
		self.next1 = gtk.Button("next")
		self.next1.connect("clicked",self.cont1)
		self.next2 = gtk.Button("next")
		self.next2.connect("clicked",self.cont2)
		self.next3 = gtk.Button("next")
		self.next3.connect("clicked",self.cont3)
		self.export = gtk.Button("export")
		self.export.connect("clicked",self.cfg)
		hbox.add(cancel)
		hbox.add(self.next1)
		hbox.add(self.next2)
		hbox.add(self.next3)
		hbox.add(self.export)
		halign = gtk.Alignment(1, 0, 0, 0)
		halign.add(hbox)
		

		#checkbox buttons
		self.b_trackpad = gtk.CheckButton("Enable trackpad")
		self.b_lefthanded = gtk.CheckButton("Enable left-handed")

		#pressure curve options
		self.cb_label = gtk.Label("pressure curve:")
		self.cb_pressure = gtk.combo_box_new_text()
		self.cb_pressure.set_size_request(120,32)
		self.cb_pressure.append_text('linear')
		self.cb_pressure.append_text('soft')
		self.cb_pressure.append_text('hard')
		self.cb_pressure.set_active(0)


		#target offset settings
		self.offset_lbox = gtk.Label("monitor offset:")
		self.offset_box = gtk.HBox(False, 6)
		self.offset_x = gtk.Entry()
		self.offset_x.set_size_request(24,32)
		self.offset_x.set_text("0")
		self.offset_y = gtk.Entry()
		self.offset_y.set_text("0")
		self.offset_y.set_size_request(24,32)
		self.offset_lx = gtk.Label("x:")
		self.offset_ly = gtk.Label("y:")
		self.offset_box.add(self.offset_lx)
		self.offset_box.add(self.offset_x)
		self.offset_box.add(self.offset_ly)
		self.offset_box.add(self.offset_y)

		#target monitor dimensions
		self.dim_lbox = gtk.Label("target monitor dimensions:")
		self.dim_box = gtk.HBox(False, 6)
		self.dim_x = gtk.Entry()
		self.dim_x.set_text(str(gtk.gdk.screen_width()))
		self.dim_x.set_size_request(24,32)
		self.dim_y = gtk.Entry()
		self.dim_y.set_text(str(gtk.gdk.screen_height()))
		self.dim_y.set_size_request(24,32)
		self.dim_lx = gtk.Label("w:")
		self.dim_ly = gtk.Label("h:")
		self.dim_box.add(self.dim_lx)
		self.dim_box.add(self.dim_x)
		self.dim_box.add(self.dim_ly)
		self.dim_box.add(self.dim_y)

		self.btn = [0,1,2,3,4,5,6]
		self.b = [0,1,2,3,4,5,6]

		# btn configs
		lalign = gtk.Alignment(0, 0, 0, 0)
		self.btn[0] = [1,2,3,4]
		self.b[0] = gtk.HBox(True, 3)
		self.btn[0][0] = gtk.Label("BUTTONS")
		self.btn[0][1] = gtk.Label("mod1")
		self.btn[0][2] = gtk.Label("mod2")
		self.btn[0][3] = gtk.Label("key")
		self.b[0].add(self.btn[0][0])
		self.b[0].add(self.btn[0][1])
		self.b[0].add(self.btn[0][2])
		self.b[0].add(self.btn[0][3])

		for i in range(1,7):
			self.btn[i] = [1,2,3,4]
			self.b[i] = gtk.HBox(True, 3)
			self.btn[i][0] = gtk.Label("btn"+str(i))
			self.btn[i][1] = clone_widget("mod")
			self.btn[i][2] = clone_widget("mod")
			self.btn[i][3] = clone_widget("key")
			self.b[i].add(self.btn[i][0])
			self.b[i].add(self.btn[i][1])
			self.b[i].add(self.btn[i][2])
			self.b[i].add(self.btn[i][3])


		self.gst = [0,1,2,3,4,5,6,7,8,9,10]
		self.g = [0,1,2,3,4,5,6,7,8,9,10]

		# gst configs
		self.gst[0] = [1,2,3,4]
		self.g[0] = gtk.HBox(True, 3)
		self.gst[0][0] = gtk.Label("GESTURES")
		self.gst[0][1] = gtk.Label("mod1")
		self.gst[0][2] = gtk.Label("mod2")
		self.gst[0][3] = gtk.Label("key")
		self.g[0].add(self.gst[0][0])
		self.g[0].add(self.gst[0][1])
		self.g[0].add(self.gst[0][2])
		self.g[0].add(self.gst[0][3])

		for i in range(1,11):
			self.gst[i] = [1,2,3,4]
			self.g[i] = gtk.HBox(True, 3)
			self.gst[i][0] = gtk.Label(gst_list[i-1])
			self.gst[i][1] = clone_widget("mod")
			self.gst[i][2] = clone_widget("mod")
			self.gst[i][3] = clone_widget("key")
			self.g[i].add(self.gst[i][0])
			self.g[i].add(self.gst[i][1])
			self.g[i].add(self.gst[i][2])
			self.g[i].add(self.gst[i][3])

		#export name
		self.ex_box = gtk.HBox(False, 3)
		self.ex_l1 = gtk.Label("export as: ")
		self.ex_name = gtk.Entry()
		self.ex_name.set_text("settings.py")
		self.ex_box.add(self.ex_l1)
		self.ex_box.add(self.ex_name)


		#gtk, putting everything together
		self.page1.pack_start(self.b_trackpad, False, False, 3)
		self.page1.pack_start(self.b_lefthanded, False, False, 3)
		
		#leave fine tuning pressure adjustment to the art software
		#self.page1.pack_start(cb_label, False, False, 3)
		#self.page1.pack_start(cb_pressure, False, False, 3)
		self.page1.pack_start(self.offset_lbox, False, False, 3)
		self.page1.pack_start(self.offset_box, False, False, 3)
		self.page1.pack_start(self.dim_lbox, False, False, 3)
		self.page1.pack_start(self.dim_box, False, False, 3)


		self.page2 = gtk.VBox(False, 5)
		for i in range(0,7):
			self.page2.pack_start(self.b[i], False, False, 3)

		self.page3 = gtk.VBox(False, 5)
		for i in range(0,11):
			self.page3.pack_start(self.g[i], False, False, 3)

		self.page4 = gtk.VBox(False, 5)
		self.page4.pack_start(self.ex_box,False,False,3)

		vbox.pack_start(self.page1, False, False, 8)
		vbox.pack_start(self.page2, False, False, 8)
		vbox.pack_start(self.page3, False, False, 8)
		vbox.pack_start(self.page4, False, False, 8)

		# vbox.pack_start(align_bottom)
		vbox.pack_end(halign, False, False, 3)

		self.add(vbox)
		self.show_all()
		self.page2.hide()
		self.page3.hide()
		self.page4.hide()
		self.next2.hide()
		self.next3.hide()
		self.export.hide()

	def pressure_changed(self, widget):
		PRESSURE = widget.get_active_text()
	def quit(self,widget,data=None):
		gtk.main_quit()

	def cont1(self,widget,data=None):
		self.page1.hide()
		self.next1.hide()
		self.page2.show()
		self.next2.show()
	def cont2(self,widget,data=None):
		self.page2.hide()
		self.next2.hide()
		self.page3.show()
		self.next3.show()
	def cont3(self,widget,data=None):
		self.page3.hide()
		self.next3.hide()
		self.page4.show()
		self.export.show()

	def cfg(self,widget,data=None):
		conf = open(self.ex_name.get_text(),"w+")
		conf.write("from evdev import ecodes \nimport time\n\n")
		conf.write("TRACKPAD_ENABLED = " + str(self.b_trackpad.get_active()) + "\n")

		conf.write("LEFT_HANDED = " + str(self.b_lefthanded.get_active()) + "\n")
		conf.write("PRESSURE_CURVE = False \n")
		conf.write("FULL_PRESSURE = 1.0 \n")
		conf.write("MONITOR_X = " + str(self.offset_x.get_text()) + "\n")
		conf.write("MONITOR_Y = " + str(self.offset_y.get_text()) + "\n")
		conf.write("MONITOR_W = " + str(self.dim_x.get_text()) + "\n")
		conf.write("MONITOR_H = " + str(self.dim_y.get_text()) + "\n\n")

		for i in range (1,7):
			conf.write("def btn" + str(i) + "(vbtn):\n")
			num_keys = 0
			key = [0,1,2]
			for j in range(1,4):
				key[j-1] = self.btn[i][j].get_active_text()
				if key[j-1] != '':
					conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_" + key[j-1] + ", 1)\n")
					num_keys += 1
			for j in range(1,4):
				if key[j-1] != '':
					conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_" + key[j-1] + ", 0)\n")
			if num_keys == 0:
				conf.write("	pass\n\n")
			else: 
				conf.write("	vbtn.syn()\n\n")

		conf.write("def btn0(vbtn):\n")
		conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)\n")
		conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)\n")
		conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)\n")
		conf.write("	vbtn.syn()\n\n")

		for i in range (1,11):
			conf.write("def gst" + str(i) + "(vbtn):\n")
			num_keys = 0
			key = [0,1,2]
			for j in range(1,4):
				key[j-1] = self.gst[i][j].get_active_text()
				if key[j-1] != '':
					conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_" + key[j-1] + ", 1)\n")
					num_keys += 1
			for j in range(1,4):
				if key[j-1] != '':
					conf.write("	vbtn.write(ecodes.EV_KEY, ecodes.KEY_" + key[j-1] + ", 0)\n")
			if num_keys == 0:
				conf.write("	pass\n\n")
			else: 
				conf.write("	vbtn.syn()\n\n")


		conf.write("def gst0(vbtn):\n")
		conf.write("	pass\n\n")

		conf.close()
		gtk.main_quit()

def clone_widget(type):
	btn= gtk.combo_box_new_text()
	if type == "mod":
		btn.append_text('')
		btn.append_text('LEFTCTRL')
		btn.append_text('LEFTALT')
		btn.append_text('LEFTSHIFT')
		btn.set_active(0)
		return btn
	else:
		for key in keys:
			btn.append_text(key)

		btn.set_active(0)
		return btn

keys = [
	'',
	'A',
	'B',
	'C',
	'D',
	'E',
	'F',
	'G',
	'H',
	'I',
	'J',
	'K',
	'L',
	'M',
	'N',
	'O',
	'P',
	'Q',
	'R',
	'S',
	'T',
	'U',
	'V',
	'W',
	'Y',
	'X',
	'Z',
	'SPACE',
	'1',
	'2',
	'3',
	'4',
	'5',
	'6',
	'7',
	'8',
	'9',
	'0',
	'MINUS',
	'EQUAL',
	'TAB',
	'LEFTBRACE',
	'RIGHTBRACE',
	'SEMICOLON',
	'APOSTROPHE',
	'GRAVE',
	'BACKSLASH',
	'COMMA',
	'DOT',
	'SLASH',
	'LEFT',
	'RIGHT',
	'UP',
	'DOWN',
	'PAGEUP',
	'PAGEDOWN',
	'INSERT',
	'BACKSPACE',
	'ENTER',
	'ESC',
	'DELETE'
]

gst_list = [
	'<< ',
	'>> ',
	'^^ ',
	'vv ',
	'<<<',
	'>>>',
	'^^^',
	'vvv',
	'<> ',
	'>< ',
]

PinWiz()
gtk.main()


