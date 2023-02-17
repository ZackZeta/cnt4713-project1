#!/usr/bin/env python3

import sys

#importing socket
import socket

#if __name__ == '__main__':
#    sys.stderr.write("client is not implemented yet\n")
    
    
#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#remote connect to ((hostname, port))
sock.connect(("127.0.0.1", 65432))

#sending initial buffer
#b symbol buffer
#ASCII control characters:(\r) Carriage Return and (\n) Line Feed.
#used in many protocols to separate header and body fields, when text is sent between systems.
l = sock.send(b"foobar\r\n")
print("send bytes", l)

b = sock.recv(1024)
print("Received: '%s'" % b)
