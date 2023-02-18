import sys

#importing socket
import socket
print("client is running")

#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(sock)

sock.connect(("127.0.0.1", 12345))

l = sock.send(b"foobar\r\n")
print("send bytes", l)

b = sock.recv(1024)
print("Received: '%s" % b)
