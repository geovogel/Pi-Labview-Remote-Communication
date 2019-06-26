#!/usr/bin/python
# Written for Python version 2.7
# An improved Hello World server that does not hang the port when terminated
# Binds REP socket to tcp://*:5555
# Expects b"Hello" from client, replies with b"World"
 
import time
import zmq
print 'pyzmq version: ', zmq.pyzmq_version()

# Initialize PyZMQ socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print "Server running..."

try:
    while True:
        try:      
            message = socket.recv(zmq.NOBLOCK) # Check for request from client
            print("Received request: %s" % message)
            socket.send(b"World")   # Send reply back to client if message received
        except zmq.ZMQError as e:   # Allow for NOBLOCK error for no message
            pass
        time.sleep(.1)
except KeyboardInterrupt:           # Graceful Ctrl-C program termination 
    print "Quit request received..."
    print "Cleaning up and exiting server."
    socket.close()                  # Close socket to release TCP binding
    context.term()




      

