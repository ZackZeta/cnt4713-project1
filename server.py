#!/usr/bin/env python3

import sys
import socket
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def clientHandling(conn, addr, file_dir, file_count, file_name=None):
    conn.send(b'accio\r\n')
    # Create the file name based on the number of files in the folder
    file_name = os.path.join(file_dir, str(file_count+1) + ".file")

    with open(file_name, "wb") as f:
        data = conn.recv(1024)
        # Set the initial time value to the current time
        start_time = time.monotonic()
        while data:
            f.write(data)
            # Update the time value each time new data is received
            start_time = time.monotonic()
            data = conn.recv(1024)
            # Check if no new data has been received for more than 10 seconds
            if time.monotonic() - start_time > 10:
                # Close the connection and delete the partially received file
                conn.close()
                os.remove(file_name)
                # Write an error message to the file
                with open(file_name, "wb") as error_file:
                    error_file.write(b"ERROR: Connection timed out after 10 seconds")
                return file_count

    # Increment the file count
    file_count += 1
    return file_count

def main(port, file_dir, filename=None):
    if port < 1 or port > 65535:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)

    if filename is None:
        filename = "defaultFile"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
        except OSError:
            sys.stderr.write("ERROR: Port %d is already in use\n" % port)
            sys.exit(1)
        
        s.listen(20)
        print("Listening on {}:{}".format('0.0.0.0', port))

        file_count = 1
        thread_count = 0
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                conn, addr = s.accept()
                with lock:
                    thread_count += 1
                    executor.submit(clientHandling, conn, addr, file_dir, filename, file_count)
                    file_count += 1

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Accio Server')
    parser.add_argument('port', type=int, help='Port number to listen on')
    parser.add_argument('file_dir', help='Directory to save received files')
    args = parser.parse_args()

    main(args.port, args.file_dir)