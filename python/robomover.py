#import Xlib.display as display
#import Xlib.X as X
import tkinter as tk
from Maestro import Controller
import time


motors = 1
full_turn = 0
body = 2
h_turn = 3
h_tilt = 4

default_speed = 10
default_accel = 10
default_pos = 6000

class KeyController():
	def __init__(self,win):
		self.root = win
		self.tango = Controller()
		self.body = default_pos
		self.headturn = default_pos
		self.headtilt = default_pos
		self.motors = 0
		self.turn = 0
		self.tango.setAccel(motors, default_accel)
		self.tango.setAccel(full_turn,default_accel)
		for i in range(1,6):
			self.tango.setTarget(i,default_pos)
		
	def arrow(self,key):
		print(key.keycode)
		#print(self.motors)
		offsetPos = default_pos + self.motors
		offsetNeg = default_pos - self.motors
		print(offsetPos)
		if (self.motors > 0):
			if key.keycode == 116:
				self.tango.setTarget(motors, offsetPos)
			elif key.keycode == 111:
				self.tango.setTarget(motors, offsetNeg)
		else:
			self.tango.setTarget(motors, default_pos)	
			
		if key.keycode == 113:
			self.tango.setTarget(full_turn, int(default_pos + self.motors))
		elif key.keycode == 114:
			self.tango.setTarget(full_turn, int(default_pos - self.motors))	
			
		if key.keysym == 'c':
			for i in range(2):
				self.tango.setTarget(i,default_pos)
			self.body = 0
			self.motors = 0
		if key.keysym == 'i':
			self.motors += 400
			if self.motors > 1200:
				self.motors = 1200
		if key.keysym =='k':
			self.motors -= 400
			if self.motors < 0:
				self.motors = 0
		if key.keysym == 'j':
			self.body += 300
			if self.body > 7500:
				self.body = 7500
			self.tango.setTarget(body, self.body)
		elif key.keysym =='l':
			self.body -= 300
			if self.body < 4500:
				self.body = 4500
			self.tango.setTarget(body, self.body)
		if key.keysym == 'w':
			self.headtilt += 300
			if self.headtilt > 7500:
				self.heatilt = 7500
			self.tango.setTarget(h_tilt, self.headtilt)
		elif key.keysym =='s':
			self.headtilt -= 300
			if self.headtilt < 4500:
				self.headtilt = 4500
			self.tango.setTarget(h_tilt, self.headtilt)
		if key.keysym == 'a':
			self.headturn += 300
			if self.headturn > 7500:
				self.headturn = 7500
			self.tango.setTarget(h_turn, self.headturn)
		elif key.keysym =='d':
			self.headturn -= 300
			if self.headturn < 4500:
				self.headturn = 4500
			self.tango.setTarget(h_turn, self.headturn)
		elif key.keysym == 'r':
			for i in range(6):
				self.tango.setTarget(i,default_pos)
			self.body = default_pos
			self.headturn = default_pos
			self.headtilt = default_pos
			self.motors = 0
			self.turn = 0
		#print(self.motors)
		time.sleep(.1)
		#print(self.tango.getPosition(motors))
		#self.tango.setTarget(motors, self.motors)
		
	
	'''def release(self, key):
		if key.keycode == 111 or key.keycode == 116:
			self.tango.setTarget(motors, default_pos)
			print(self.tango.getPosition(motors))'''
		
		

win = tk.Tk()
keys = KeyController(win)
win.bind('<Up>', keys.arrow) # 111
win.bind('<Down>', keys.arrow) # 116
win.bind('<Left>', keys.arrow) # 113
win.bind('<Right>', keys.arrow) # 114

win.bind('<i>', keys.arrow)
win.bind('<j>', keys.arrow)
win.bind('<k>', keys.arrow)
win.bind('<l>', keys.arrow)

win.bind('<w>', keys.arrow)
win.bind('<a>', keys.arrow)
win.bind('<s>', keys.arrow)
win.bind('<d>', keys.arrow)
win.bind('<f>', keys.arrow)
win.bind('<g>', keys.arrow)

win.bind('<r>', keys.arrow)
win.bind('<x>', keys.arrow)
win.bind('<c>', keys.arrow)


'''release handling'''
'''
win.bind('<KeyRelease-Up>', keys.arrow) # 111
win.bind('<KeyRelease-Down>', keys.arrow) # 116
win.bind('<KeyRelease-Left>', keys.arrow) # 113
win.bind('<KeyRelease-Right>', keys.arrow) # 114

win.bind('<KeyRelease-i>', keys.release)
win.bind('<KeyRelease-j>', keys.release)
win.bind('<KeyRelease-k>', keys.release)
win.bind('<KeyRelease-l>', keys.release)

win.bind('<KeyRelease-w>', keys.release)
win.bind('<KeyRelease-a>', keys.release)
win.bind('<KeyRelease-s>', keys.release)
win.bind('<KeyRelease-d>', keys.release)
win.bind('<KeyRelease-f>', keys.release)
win.bind('<KeyRelease-g>', keys.release)

win.bind('<KeyRelease-z>', keys.release)
win.bind('<KeyRelease-x>', keys.release)
win.bind('<KeyRelease-c>', keys.release)
'''
#d = display.Display()
#d.change_keyboard_control(auto_repeat_mode=X.AutoRepeatModeOff)
#x = d.get_keyboard_control()

win.mainloop()
