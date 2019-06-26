#!/usr/bin/python
# Written for Python version 2.7
# Hello World server in Python
# Binds REP socket to tcp://*:5555
# Expects b"Hello" from client, replies with b"World"
 
import time
import zmq
print 'pyzmq version: ', zmq.pyzmq_version()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print "Server running."
while True:
    message = socket.recv() #Wait for next request from client
    print("Received request: %s" % message)
    socket.send(b"World") #  Send reply back to client       
    time.sleep(.1)


      

