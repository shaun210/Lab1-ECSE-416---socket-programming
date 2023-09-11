import socket
import os

HOST = "127.0.0.1"
PORT = 12345 


# Create a socket object and set default protocol to TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# associate the socket with a specific network interface and port number to list for incoming connections
server_socket.bind((HOST, PORT))

# queue of 5 incoming connections
server_socket.listen(5)

while True:
    
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    request_data = client_socket.recv(4096).decode()
    parts = request_data.split()
    filename = parts[1].lstrip('/')
    print(f"Received filename: {filename}")

    if not os.path.exists(filename):
        response = f"HTTP/1.0 404 NOT FOUND\r\n\r\n"
        client_socket.sendall(response.encode())
    #  if exist, must send status and file in single request
    else:
        file = open(filename, 'r')
        file_data = file.read()
        response = (f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_data)}\r\n\r\n" + file_data).encode()

        client_socket.sendall(response)
        
    client_socket.close()