#/usr/bin/env python3

import sys

#importing socket
import socket

#if __name__ == '__main__':
#    sys.stderr.write("server is not implemented yet\n")

#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(sock)

sock.bind(("localhost", 12345))
print(sock)

socket.listen(1)
clientSocket, ClientAddress = sock.accept()