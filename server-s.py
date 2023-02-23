#/usr/bin/env python3

import sys
import socket
import signal
import threading
import time

def signalHandler(signum, frame):
    global not_stopped
    not_stopped = False

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
    
    # Process the header and get the filename and file size
    lines = header.split(b'\r\n')
    filename = lines[0].split(b' ')[1]
    filesize = int(lines[1].split(b' ')[1])
    
    # Receive the file data and save it to a file
    with open(filename, "wb") as f:
        bytes_received = 0
        while bytes_received < filesize:
            data = conn.recv(min(1024, filesize - bytes_received))
            if not data:
                break
            f.write(data)
            bytes_received += len(data)
    
    # Send a response back to the client indicating that the file was received and saved
    response = f"File '{filename.decode()}' of size {filesize} bytes received and saved successfully".encode()
    conn.send(response)
    
    # Close the connection
    conn.close()

def main():
    global not_stopped
    not_stopped = True
    
    # Parse command line arguments
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
        if port < 0 or port > 65535:
            sys.stderr.write("ERROR: Invalid port number\n")
            sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)
    
    # Set up a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)
    
    # Set up signal handlers to handle SIGINT, SIGQUIT, and SIGTERM
    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGQUIT, signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)
    
    # Loop to accept incoming connections
    while not_stopped:
        conn, addr = server_socket.accept()
        print(f"Connection received from {addr}")
        
        # Create a new thread to handle the connection and pass it to the processing function
        t = threading.Thread(target=processClientConnection, args=(conn, addr))
        t.start()
        
    # Close the server socket
    server_socket.close()

if __name__ == '__main__':
    main()