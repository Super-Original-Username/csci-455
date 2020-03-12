import tkinter as tk 
import queue
from Maestro import Controller
import time
# from pololu import maestro as ms

action_queue = queue.Queue()
queue_string = 'Current Queue: '
action_string = 'Current Action: '

motors = 1
full_turn = 0
body = 2
h_turn = 3
h_tilt = 4

default_speed = 10
default_accel = 10
default_pos = 6000

class ButtonController():
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

                
    def t1(self):                               # Head Tilt
        self.tango.setTarget(h_tilt, 7000)
        self.tango.setTarget(h_tilt, 5000)
        self.tango.setTarget(h_tilt, 6000)


    def t2():                               # Head Turn
        self.tango.setTarget(h_turn, 7000)
        self.tango.setTarget(h_turn, 5000)
        self.tango.setTarget(h_turn, 6000)


    def t3():                               # Torso Turn
        self.tango.setTarget(body, 7000)
        self.tango.setTarget(body, 5000)
        self.tango.setTarget(body, 6000)


    def t4():                               # Forward (7000) for 1.5s
        self.tango.setTarget(motors, 7000)
        time.sleep(1.5)
        self.tango.setTarget(motors, 6000)


    def t5():                               # Backwards(5000) for 1.5s
        self.tango.setTarget(motors, 5000)
        time.sleep(1.5)
        self.tango.setTarget(motors, 6000)


    def t6():                               # Turn clockwise
        print(6)


    def t7():                               # Turn counter-clockwise
        print(7)



def line_up(fn):
    global queue_string
    print(fn)
    print(move_dict[fn].__name__)
    if type(fn) is str:
        action_queue.put(fn)
        queue_string = queue_string + '->' + move_dict[fn].__name__
        lab.configure(text=queue_string)
        #win.update()


def go():
    while not action_queue.empty():
        action = action_queue.get()
        print(move_dict[action].__name__)

        move_dict[action]
        time.sleep(1.5)



move_dict = {'htilt':t1,'hrot':t2,'trot':t3,'fw':t4,'bw':t5,'cw':t6,'ccw':t7}


win = tk.Tk()
buttons = ButtonController(win)
#win.attributes('-fullscreen',True) # this *should* just maximize the window. Otherwise uncomment the below line and adjust to fit
win.geometry("1280x720")
btn_box =tk.Frame(win)
btn_box.pack()

head_tilt_btn = tk.Button(btn_box,text="Head Tilt", command =lambda: line_up('htilt'))
head_tilt_btn.grid(padx=25, pady=10, row=3, column=0) 

head_rot_btn = tk.Button(btn_box,text="Head Rotation", command =lambda: line_up('hrot'))
head_rot_btn.grid(padx=25, pady=10, row=3, column=1) 

tors_rot_btn = tk.Button(btn_box,text="Torso Rotation", command =lambda: line_up('trot'))
tors_rot_btn.grid(padx=25, pady=10, row=3, column=2) 

fw_btn = tk.Button(btn_box,text="Move Forward", command =lambda: line_up('fw'))
fw_btn.grid(padx=25, pady=10, row=3, column=3) 

bw_btn = tk.Button(btn_box,text="Move Backward", command =lambda: line_up('bw'))
bw_btn.grid(padx=25, pady=10, row=3, column=4) 

cw_btn = tk.Button(btn_box,text="Turn Clockwise", command =lambda: line_up('cw'))
cw_btn.grid(padx=25, pady=10, row=3, column=5) 

ccw_btn = tk.Button(btn_box,text="Turn Counter-clockwise", command =lambda: line_up('ccw'))
ccw_btn.grid(padx=25, pady=10, row=3, column=6) 

go_btn = tk.Button(btn_box,text="Run Program", command = go)
go_btn.grid(padx=25, pady=10, row=5, column=3) s

#close_btn = tk.Button(btn)

lab = tk.Label(btn_box,text=queue_string)
lab.grid(padx=20, pady=10, row=2, column=3) 

'''
head_tilt_btn = tk.Button(btn_box,text="Head Tilt", command = line_up(9))
head_tilt_btn.pack()
'''

win.mainloop()
