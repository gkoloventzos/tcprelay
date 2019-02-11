#!/usr/bin/env python

import sys
import socket
import thread
import signal

NET_MSG_SIZE = 4096

signal.signal(signal.SIGINT, signal.default_int_handler)
def usage():
    print "Usage: ./relayserver [port] <msg_size>"
    sys.exit(1)

# Purpose: create new socket
# Input: string hostname and int port number
# Output: socket or exception with error message
def createNewSocket(hostname, socket_port):
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((hostname, socket_port))
        s.listen(5)
    except socket.error, (value, message):
        if s:
            s.close()
            print "Could not open socket: " + message
            sys.exit(1)
    return s


# Method to handle Server connection
def handleServer(server_sock, relayhost, relayport):

    # Set params for tunnel host and port
    tunnelhost = relayhost
    tunnelport = relayport + 1

    # Create new tunnel socket
    tunnelsocket = createNewSocket(tunnelhost, tunnelport)

    # Form message and send back to the echoserver
    tunnel_msg = tunnelhost + ":" + str(tunnelport)
    server_sock.send(tunnel_msg)

    # Accept connection
    tunnelclient, tunnelclientaddr = tunnelsocket.accept()

    running = 1
    try:
        while running:
	    # Receive data from the tunnel client
            tunnelclientdata = tunnelclient.recv(NET_MSG_SIZE)
            if tunnelclientdata:
	        # Forward data to echo server
                server_sock.send(tunnelclientdata)
	        # Receive replay back from echo server
                serverdata = server_sock.recv(NET_MSG_SIZE)
                if serverdata:
	            # Forward reply back to tunnel client
                    tunnelclient.send(serverdata)
                else:
                    running = 0
            else:
                running = 0
    except KeyboardInterrupt:
        running = 0

    tunnelsocket.close()
    server_sock.close()

# Method to create a new relay server
def createRelayServer(relayhost, relayport):
    relaysocket = createNewSocket(relayhost, relayport)

    running = 1
    try:
        while running:
            # Accept connection
            new_socket, addr = relaysocket.accept()
	    # Spawn a new thread for connection
            thread.start_new_thread(handleServer, (new_socket, relayhost, relayport))
    except KeyboardInterrupt:
        print "Terminating Server"
        running = 0

if __name__ == '__main__':
    host = 'localhost'
    port = ''

    # Check command line arguments
    total = len(sys.argv)
    if total < 2 or total > 3:
        usage()

    if not sys.argv[1].isdigit():
        print "first argument"
        usage()

    port = int(sys.argv[1])
    if total == 3:
        if sys.argv[2].isdigit():
            NET_MSG_SIZE = int(sys.argv[2])
            if not NET_MSG_SIZE:
                usage()
        else:
            print "Message size not int"
            usage()
    if not port:
        usage()

    createRelayServer(host, port)
