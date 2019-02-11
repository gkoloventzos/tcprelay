#!/usr/bin/env python

import socket

def relay(host, port):

    # Connect to the relay server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Receive a tunnel host & port information
#    data = s.recv(size)

#    print data
    return s
