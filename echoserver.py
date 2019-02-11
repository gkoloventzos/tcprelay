#!/usr/bin/env python

import sys
import socket
import relaylibrary

def usage():
    print "Usage: ./echoserver [relay host] [relay port]"
    sys.exit(1)

if __name__ == '__main__':
    host = ''
    port = ''
    size = 4096

    # Check command line arguments
    total = len(sys.argv)
    if total < 3:
        usage()

    host = sys.argv[1]
    if sys.argv[2].isdigit():
        port = int(sys.argv[2])
    else:
        usage()

    if not (host or port):
        usage()

    # Connect to the relay server
    s = relaylibrary.relay(host, port)

    # Receive a tunnel host & port information
    data = s.recv(size)

    print data

    # Now receive any packets from the relay server and send back
    running = 1
    while running:
        data = s.recv(size)
        if data:
            s.send(data)
        else:
            running = 0

    s.close()
