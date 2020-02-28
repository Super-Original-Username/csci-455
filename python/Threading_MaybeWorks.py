#import tkinter as tk
import threading
import time
#from robomover import KeyController
import socket

class Sender(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.socket.sendall("To Hell with this".encode())
        self.socket.end()


class Listener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.msg = self.socket.recv(1024)
        print(self.msg)
        
        
def __main__():
##    win = tk.Tk()
##    keys = KeyController(win)
##    win.bind('<Up>', keys.arrow) # 111
##    win.bind('<Down>', keys.arrow) # 116
##    win.bind('<Left>', keys.arrow) # 113
##    win.bind('<Right>', keys.arrow) # 114
##
##    win.bind('<i>', keys.arrow)
##    win.bind('<j>', keys.arrow)
##    win.bind('<k>', keys.arrow)
##    win.bind('<l>', keys.arrow)
##
##    win.bind('<w>', keys.arrow)
##    win.bind('<a>', keys.arrow)
##    win.bind('<s>', keys.arrow)
##    win.bind('<d>', keys.arrow)
##    win.bind('<f>', keys.arrow)
##    win.bind('<g>', keys.arrow)
##
##    win.bind('<r>', keys.arrow)
##    win.bind('<x>', keys.arrow)
##    win.bind('<c>', keys.arrow)


##    '''release handling'''
##    '''
##    win.bind('<KeyRelease-Up>', keys.arrow) # 111
##    win.bind('<KeyRelease-Down>', keys.arrow) # 116
##    win.bind('<KeyRelease-Left>', keys.arrow) # 113
##    win.bind('<KeyRelease-Right>', keys.arrow) # 114
##
##    win.bind('<KeyRelease-i>', keys.release)
##    win.bind('<KeyRelease-j>', keys.release)
##    win.bind('<KeyRelease-k>', keys.release)
##    win.bind('<KeyRelease-l>', keys.release)
##
##    win.bind('<KeyRelease-w>', keys.release)
##    win.bind('<KeyRelease-a>', keys.release)
##    win.bind('<KeyRelease-s>', keys.release)
##    win.bind('<KeyRelease-d>', keys.release)
##    win.bind('<KeyRelease-f>', keys.release)
##    win.bind('<KeyRelease-g>', keys.release)
##
##    win.bind('<KeyRelease-z>', keys.release)
##    win.bind('<KeyRelease-x>', keys.release)
##    win.bind('<KeyRelease-c>', keys.release)
##    '''
##    #d = display.Display()
##    #d.change_keyboard_control(auto_repeat_mode=X.AutoRepeatModeOff)
##    #x = d.get_keyboard_control()

    client = socket.socket()
    client.connect(("10.200.28.219", 8080))
    time.sleep(1)
    #client.send("Client Connected".encode())
    sendThread = Sender(client)
    recThread = Listener(client)
    
    Flag = True
    
    # New Thread
    try:
        sendThread.start()
    except:
        print("Error: unable to send connection confirmation")

    try:
        recThread.start()
    except:
        print("Error: cannot receive from server")
        Flag = False

    # Continue Thread
##    while(Flag):
##        try:
##            recThread.start()
##        except:
##            print("Error: cannot receive from server")
##            Flag = False
##        pass
   # win.mainloop()
    client.close()

__main__()
