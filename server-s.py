#!/usr/bin/env python3

import sys
import socket
import signal
import threading
from concurrent.futures import ThreadPoolExecutor

def signalHandler(sig, frame):
    global server_socket
    #print("Exiting server...")
    server_socket.close()
    sys.exit(0)

def processClientConnection(conn, addr):
    # Timeout after 60 seconds of inactivity
    try:
        conn.settimeout(60)
    except socket.error:
        conn.send(b"Error occurred while setting timeout. Closing connection.\r\n")
        conn.close()
        return
    conn.send(b'accio\r\n')

    # Receive the file header
    header = b''
    while True:
        data = conn.recv(1024)
        if not data:
            conn.send(b"Invalid header received. Closing connection.\r\n")
            conn.close()
            return
        header += data
        if b'\r\n\r\n' in header:
            # Process the header and get the filename and file size
            lines = header.split(b'\r\n')
            filename_line = lines[0].split(b' ')
            if len(filename_line) < 2 or filename_line[1] == b'':
                conn.send(b"Invalid header received. Closing connection.\r\n")
                conn.close()
                return
            filename = filename_line[1]
            if b'filesize=' not in header:
                filesize = 0 # or some other default value
                conn.send(b"Warning: file size not specified in header. Using default file size.\r\n")
            else:
                filesize = int(lines[1].split(b' ')[1])
            break

    # If header is empty or incomplete, send an error response and close the connection
    if not header or b'filename=' not in header or b'filesize=' not in header:
        conn.send(b"Invalid header received. Closing connection.\r\n")
        conn.close()
        return

    # Receive the file data and save it to a file
    with open(f"./{filename.decode()}", "wb") as f:
        bytes_received = 0
        while bytes_received < filesize:
            data = conn.recv(min(1024, filesize - bytes_received))
            if not data:
                conn.send(f"File '{filename.decode()}' of size {bytes_received} bytes transfer interrupted. File transfer aborted.\r\n".encode())
                conn.close()
                return
            f.write(data)
            bytes_received += len(data)

    # Send a response back to the client indicating that the file was received and saved
    response = f"File {filename.decode()} of size {filesize} bytes received and saved successfully\r\nAccio File Transfer Complete!\r\n".encode()
    conn.send(response)

    # Close the connection
    conn.close()

def main():
    global server_socket
    executor = ThreadPoolExecutor(max_workers=20)
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
    
    # Set up a signal handler to handle SIGINT
    signal.signal(signal.SIGINT, signalHandler)
    
    # Loop to accept incoming connections
    while True:
        # Wait for a connection
        try:
            conn, addr = server_socket.accept()
        except OSError:
            # server_socket has been closed, exit the loop
            break
        print(f"Connection received from {addr}")
        
        # Create a new thread to handle the connection and pass it to the processing function
        t = threading.Thread(target=processClientConnection, args=(conn, addr))
        t.start()
    
    # Close the server socket
    server_socket.close()
    

if __name__ == '__main__':
    main()