import sys

"""
#importing socket
import socket

print("server is running")

#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(sock)
sock.bind(("localhost", 12345))
print(sock)

print("test1")

sock.listen(1)
clientSocket, ClientAddress = sock.accept()

print("test2")

print("Accepted connection from", ClientAddress)

print("test3")
data = clientSocket.recv(1024)
print(f"Received: {data.decode()}")

print("test4")

clientSocket.close()
sock.close()
"""

