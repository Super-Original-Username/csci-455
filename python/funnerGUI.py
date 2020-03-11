import tkinter as tk 
import queue
import time
# from pololu import maestro as ms

action_queue = queue.Queue()
queue_string = 'Current Queue: '
action_string = 'Current Action: '



def t1():
    print(1)


def t2():
    print(2)


def t3():
    print(3)


def t4():
    print(4)


def t5():
    print(5)


def t6():
    print(6)


def t7():
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
go_btn.grid(padx=25, pady=10, row=5, column=3) 

#close_btn = tk.Button(btn)

lab = tk.Label(btn_box,text=queue_string)
lab.grid(padx=20, pady=10, row=2, column=3) 

'''
head_tilt_btn = tk.Button(btn_box,text="Head Tilt", command = line_up(9))
head_tilt_btn.pack()
'''

win.mainloop()
