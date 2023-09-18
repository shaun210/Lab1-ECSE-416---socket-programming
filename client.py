import socket
import sys
import os
save_folder = 'received_image'
# this is the client socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect
dummy_increment = 0
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

    # send request
    request = f"GET /{filename} HTTP/1.1\r\n\r\n"
    client_socket.send(request.encode())
    print("Request message sent.")

    #read responce
    response = b''
    while True:
        data = client_socket.recv(1024)  # You can adjust the buffer size as needed
        if not data:
            break
        response += data

    #the b is for bytes. Allows python to read the response as bytes
    header_end_index = response.find(b"\r\n\r\n")

    # Extract the headers from the response as bytes
    headers = response[:header_end_index]

    # Extract the status line (the first line)
    status_line = headers.split(b'\r\n')[0]
     # Split the status line by spaces to extract the status code
    status_code = status_line.split(b' ')[1].decode('utf-8')

    if status_code == '404':
        print("Server HTTP Response: HTTP 404 not found")
        
    else :

        content_type = headers.split(b'\r\n')[1]
        content_type = content_type.split(b': ')[1].decode('utf-8')

        headers = response[:header_end_index].decode()

        # Process the response based on Content-Type
        if content_type == "text":
            response_body = response[header_end_index + 4:].decode('utf-8')
        else:
            response_body = response[header_end_index + 4:] # for image, use data in the form of bits.

        if status_code == '200':
            print("Request successful - 200 OK")
            print(f"Content Type: {content_type}")
            if (content_type == 'text'):
                filename_received = f"received_txt.txt"
                file_path = os.path.join(save_folder, filename_received)
                with open(file_path, 'w') as file:
                    file.write(response_body)
            else:
                filename_received = filename
                file_path = os.path.join(save_folder, filename_received)
                with open(file_path, 'wb') as file:
                    file.write(response_body)
            print("Success !!!")
        
    # elif status_code == '404':
    #     print("Server HTTP Response: HTTP 404 not found")

except socket.timeout:
    print("Timeout bruh")

finally:
    client_socket.close()
    print("socket closed.")