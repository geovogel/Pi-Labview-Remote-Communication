#!/usr/bin/python
# Written for Python version 2.7
# Hello World client in Python
# Connects a REQ socket to Hello World server using several tcp:// address forms
# Sends "Hello" to server, expects "World" back

import zmq
print 'pyzmq version:', zmq.pyzmq_version()

context = zmq.Context()
#  Do 10 requests, waiting each time for a response
def send():
    for request in range(3):
        print("Sending request %s …" % request)
        socket.send(b"Hello")

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))

#  Socket to talk to server
print('Connecting to hello world server \n')
socket = context.socket(zmq.REQ)
print("\n Connect using local network address;")
socket.connect("tcp://192.168.1.92:5555")
send()
print("\n Connect using internet address:")
socket.connect("tcp://107.207.74.104:5555")
send()
print("\n Connect using DNS address:")
socket.connect("tcp://vogelectric.net:5555")
send()


