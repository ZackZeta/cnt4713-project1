#!/usr/bin/env python3

import sys
import socket
import os
import signal
import threading
from concurrent.futures import ThreadPoolExecutor

not_stopped = True

def clientHandling(conn, addr, file_dir, file_count):
    conn.send(b'accio\r\n')
    with open(os.path.join(file_dir, str(file_count) + '.file'), 'wb') as f:
        data = conn.recv(1024)
        while data:
            f.write(data)
            data = conn.recv(1024)
    conn.close()

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False
    print("Interrupted current connection processing, waiting for next connection...")


def main(port, file_dir):
    global not_stopped

    # Register signal handlers for SIGQUIT, SIGTERM, and SIGINT signals
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    if port < 1 or port > 65535:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
        except OSError:
            sys.stderr.write("ERROR: Port %d is already in use\n" % port)
            sys.exit(1)
        
        s.listen(10)

        file_count = 1
        while not_stopped:
            conn, addr = s.accept()
            t = threading.Thread(target=clientHandling, args=(conn, addr, file_dir, file_count))
            t.start()
            file_count += 1

        # Add a loop to wait for threads to finish before exiting
        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join()

    # Wait for a signal to be received
    signal.pause()

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='Accio Server')
    parser.add_argument('port', type=int, help='Port number to listen on')
    parser.add_argument('file_dir', help='Directory to save received files')
    args = parser.parse_args()

    main(args.port, args.file_dir)
