#!/usr/bin/env python3

import socket
import os

# Constants
BUFFER_SIZE = 4096
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
FILE_PATH = "received_file.txt"

# Create a socket object
server_socket = socket.socket()

# Set socket options to reuse the address and enable TCP Keep-Alive
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# Bind the socket to a specific address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

# Receive the file size from the client
file_size_bytes = client_socket.recv(BUFFER_SIZE)
file_size = int(file_size_bytes.decode())

# Open a file for writing the received data
with open(FILE_PATH, "wb") as f:
    # Receive the file data in chunks and write them to the file
    bytes_received = 0
    while bytes_received < file_size:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        f.write(chunk)
        bytes_received += len(chunk)

    print(f"Received {bytes_received} bytes")

# Close the client socket and the server socket
client_socket.close()
server_socket.close()

print(f"File received: {FILE_PATH}")