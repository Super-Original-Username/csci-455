import tkinter as tk
import threading
import socket


def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)


def check_exec_order():


class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_draggable(self)

class DnDFrame(DragDropMixin, tk.Frame):
    pass


main = tk.Tk(width=500,height=500)

s = tk.Style()

s.configure()

h_rot_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
h_rot_frame.place(x=10, y=10)

hrlabel = tk.Label(h_rot_frame,text="head tilt")
hrlabel.pack()

h_turn_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
h_turn_frame.place(x=10, y=40)

htlabel = tk.Label(h_turn_frame,text="rotate head")
htlabel.pack()

b_right_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
b_right_frame.place(x=10, y=70)

brlabel = tk.Label(b_right_frame,text="body right")
brlabel.pack()

b_left_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
b_left_frame.place(x=10, y=100)

bllabel = tk.Label(b_left_frame,text="body left")
bllabel.pack()

arm_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
arm_frame.place(x=10, y=130)

armlabel = tk.Label(arm_frame,text="move arm")
armlabel.pack()

fw_mv_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
fw_mv_frame.place(x=10, y=160)

fwlabel = tk.Label(fw_mv_frame,text="move forward")
fwlabel.pack()

bw_mv_frame = DnDFrame(main, bg="white",cursor="dot",bd=4)
bw_mv_frame.place(x=10, y=190)

bwlabel = tk.Label(bw_mv_frame,text="move backward")
bwlabel.pack()

'''
notes = tk.Text(frame)
notes.pack()
'''

#label = DnDlabel

main.mainloop()