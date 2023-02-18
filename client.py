#importing sys
import sys
#importing socket
import socket

print("client is running")


#If statement checking to make sure 4 arguments are passed
if len(sys.argv) != 4:
    #print usage message if 4 arguments are not seen
    print("Usage: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>")
    sys.exit(1)

#client.py[0], <HOSTNAME-OR-IP>[1], <PORT>[3], <FILENAME>[4]
# set argv[1] to hostname which should be <HOSTNAME-OR-IP>  
hostname = sys.argv[1]
# set argv[2] to port which should be <PORT>. int() to convert string to int 
port = int(sys.argv[2])
# set argv[3] to filename which should be <FILENAME>
filename = sys.argv[3]

#f-string to print hostname and port supplied
print(f"Connecting to {hostname}:{port} ...")

#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting created socket to hostname and port
sock.connect((hostname, port))







#creating new socket using socket method
#socket.AF_INET for the address and protocol family for IPv4
#socket.SOCK_STREAM Stream socket type, provides dual directional communication
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print(sock)

#sock.connect(("127.0.0.1", 12345))

#l = sock.send(b"foobar\r\n")
#print("send bytes", l)

#b = sock.recv(1024)
#print("Received: '%s" % b)

