import threading
import socket

ADDR = "10.200.28.219"
PORT = 8080


class NetThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket()
        self.sock.connect((ADDR,PORT))
        self.sock.sendall("the end is nigh\n".encode())

    def run(self):
        l = Listen(self.sock)
        s = Sender(self.sock)
        l.start()
        s.start()



class Listen(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            ip = input("what:")
            ip = ip+"\n"
            self.sock.sendall(ip.encode())



class Sender(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        prev_msg = ''
        while(True):
            msg = self.sock.recv(1024)
            if msg != prev_msg:
                prev_msg = msg
                print(msg)
                #self.sock.close()

t = NetThread()
t.start()
