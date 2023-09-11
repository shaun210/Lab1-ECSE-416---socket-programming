import socket
import sys

# 2 question:

# 1. how to do: parses the request to determine the specific file being requested
# 2. what is content-type?

# this is the client socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect

if len(sys.argv) != 5:
    print("Usage: python3 client.py <host> <port> <filename> <timeout>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

filename = sys.argv[3]
timeout = int(sys.argv[4])

try:
    client_socket.settimeout(timeout)
    client_socket.connect((HOST, PORT))
    print("Connection: OK")

    request = f"GET /{filename} HTTP/1.1\r\n\r\n"
    client_socket.send(request.encode())
    print("Request message sent.")

    response = client_socket.recv(4096).decode()
    # Split the response into lines and get the first line
    status_line = response.split('\r\n')[0]

    # Parse the status line to extract the status code
    status_code = status_line.split(' ')[1]

    # Check the status code to determine the response status
    if status_code == '200':
        print("Request successful - 200 OK")
    elif status_code == '404':
        print("Server HTTP Response: HTTP 404 not found")

except socket.timeout:
    print("Timeout bruh")

finally:
    client_socket.close()
    print("socket closed.")