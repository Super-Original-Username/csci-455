import threading
import socket
import tkinter as tk

ADDR = "10.200.52.62"
PORT = 8080


class NetThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket()
        self.sock.connect((ADDR,PORT))
        #self.sock.sendall("I am alive\n".encode())

    def run(self):
        l = Listen(self.sock)
        s = Sender(self.sock)
        l.start()
        s.start()



class Sender(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            ip = input("what:")
            ip = ip+"\n"
            self.sock.sendall(ip.encode())



class Listen(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        prev_msg = ''
        while(True):
            data = self.sock.recv(1024).decode()
            if data != prev_msg:
                prev_msg = data
                print(data)
                #self.sock.close()






''' TK window thingeroos '''

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



class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_draggable(self)

class DnDFrame(DragDropMixin, tk.Frame):
    pass

main = tk.Tk()

frame = DnDFrame(main, bd=4, bg="grey")
frame.place(x=10, y=10)

notes = tk.Text(frame)
notes.pack()

''' #starts networked threads '''


t = NetThread()
t.start()
