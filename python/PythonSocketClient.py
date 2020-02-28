import tkinter as tk
import _thread
import time
import socket

##Socket socket = new Socket(server_IP,server_Port);
##s = socket.socket()         # Create a socket object
##host = socket.gethostname() # Get local machine name
##port = 12345                # Reserve a port for your service.
##
##s.connect((host, port))
##print (s.recv(1024))
##s.close()                     # Close the socket when done


# Create a TCP based client socket
echoClient =  socket.socket()

# Note: No need for bind() call in client sockets...
# Just use the socket by calling connect()
echoClient.connect(("10.200.28.219", 8080))
#echoClient.connect(("10.200.58.97", 8080));
#input("Press Enter to continue...")
time.sleep(1)
# Send affirmation
#x = input()
#echoClient.sendall(x.encode())
#echoClient.sendall(b"Client Connected")
##echoClient.close()
##time.sleep(5);
##echoClient.connect(("10.200.28.219", 8080));

msgReceived = echoClient.recv(1024)
print("At client: %s"%msgReceived.decode())
    

# Send a message
#echoClient.send("Learning Python is fun".encode());

##while (True):
##    # Get the reply
##    msgReceived = echoClient.recv(1024);
##    
##    # Print the reply
##    print("At client: %s"%msgReceived.decode());
    
echoClient.close()
