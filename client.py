# importing sys
import sys
# importing socket
import socket

#print("client is running")

def main():
    # If statement checking to make sure 4 arguments are passed
    if len(sys.argv) != 4:
        #print usage message if 4 arguments are not seen
        print("Usage: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>")
        sys.exit(1)

    # client.py[0], <HOSTNAME-OR-IP>[1], <PORT>[3], <FILENAME>[4]
    # set argv[1] to hostname which should be <HOSTNAME-OR-IP>  
    hostname = sys.argv[1]
    # set argv[2] to port which should be <PORT>. int() to convert string to int 
    port = int(sys.argv[2])
    # set argv[3] to filename which should be <FILENAME>
    filename = sys.argv[3]
    # Initialize counter variable
    accioCounter = 0
    
    # f-string to print hostname and port supplied
    #print(f"Connecting to {hostname}:{port} ...")

    # creating new socket using socket method
    # socket.AF_INET for the address and protocol family for IPv4
    # socket.SOCK_STREAM Stream socket type, provides dual directional communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connecting created socket to hostname and port
    sock.connect((hostname, port))

    # Receive initial command from server
    severReceiving = sock.recv(1024)
    # Checking if the data received is accio\r\n
    if severReceiving == b"accio\r\n":
        # increase accioCounter when data received is accio\r\n
        accioCounter = accioCounter + 1        
    else:
        # else print message and exit if it did not
        print("Did not receive 'accio\r\n' from the server")
        sys.exit(1)
        
    # Receive initial command from server
    severReceiving = sock.recv(1024)
    # Repeating checking if the data received is accio\r\n
    if severReceiving == b"accio\r\n":
        # increase accioCounter when data received is accio\r\n
        accioCounter = accioCounter + 1
    else:
        # else print message and exit if it did not
        print("Did not receive 'accio\r\n' again from the server")
        sys.exit(1)

    if accioCounter != 2:
        print("Error: Did not receive two 'accio' commands")
        sys.exit(1) 
    else:
        # Sending confirm-accio if it matches
        sock.send(b"confirm-accio\r\n")
        # Send confirm-accio-again if it matches
        sock.send(b"confirm-accio-again\r\n\r\n")

    # with statement, to handle file stream
    # open function to open file provide in argv
    # rb to read in binary file
    with open(filename, "rb") as file:
        # read first 1024 bytes of the file and store it in data
        data = file.read(1024)
        # while theres data to read
        while data:
            # send data to the server
            sock.send(data)
            # read the next 1024 bytes of the file and store it in data
            data = file.read(1024)    

    
if __name__ == "__main__":
    main()

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

