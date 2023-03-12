#!/usr/bin/env python3

import sys
import socket
import os
import signal
import threading
from concurrent.futures import ThreadPoolExecutor

def clientHandling(conn, addr, file_dir, file_count):
    with open(os.path.join(file_dir, str(file_count) + '.file'), 'wb') as f:
        data = conn.recv(1024)
        while data:
            f.write(data)
            data = conn.recv(1024)
    conn.close()

def main(port, file_dir):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
        except OSError:
            print(f"Error: Could not bind to port {port}")
            sys.exit(1)
        
        s.listen(10)

        file_count = 1
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=clientHandling, args=(conn, addr, file_dir, file_count))
            t.start()
            file_count += 1

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='Accio Server')
    parser.add_argument('port', type=int, help='Port number to listen on')
    parser.add_argument('file_dir', help='Directory to save received files')
    args = parser.parse_args()

    main(args.port, args.file_dir)