#/usr/bin/env python3

import sys
import socket
import signal
import threading

def signalHandler(sig, frame):
    print("Exiting server...")
    sys.exit(0)

def processClientConnection(conn, addr):
    # Send the "accio" command to the client
    conn.send(b'accio\r\n')
    
    # Receive the file header
    header = b''
    while b'\r\n\r\n' not in header:
        data = conn.recv(1024)
        if not data:
            break
        header += data
    
    # TODO: process the header and get the filename and file size
    
    # Receive the file data and save it to a file
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    
    # Close the connection
    conn.close()

def main():
    # Parse command line arguments
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)
    
    # Set up a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)
    
    # Set up a signal handler to handle SIGINT
    signal.signal(signal.SIGINT, signalHandler)
    
    # Loop to accept incoming connections
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection received from {addr}")
        
        # Create a new thread to handle the connection and pass it to the processing function
        t = threading.Thread(target=processClientConnection, args=(conn, addr))
        t.start()

if __name__ == '__main__':
    main()