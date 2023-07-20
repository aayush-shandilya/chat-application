import socket
import os

HOST = '192.168.55.163'  # The server's IP address
PORT = 8080  # The server's port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print('Connected to server')

buffer_size = 1024

while True:
    message = input('Enter message: ')

    if message == 'Bye':
        print('Good Bye')
        break

    if message == 'send_file':
        file_path = input('Enter file path: ')

        if not os.path.exists(file_path):
            print('File does not exist')
            continue

        # Send the file size
        file_size = os.path.getsize(file_path)
        client_socket.send(str(file_size).encode('utf-8'))

        # Send the file data in chunks
        sent_bytes = 0
        with open(file_path, 'rb') as file:
            while sent_bytes < file_size:
                # Read data from the file in chunks of buffer_size bytes
                chunk = file.read(buffer_size)
                client_socket.send(chunk)
                sent_bytes += len(chunk)
    else:
        client_socket.sendall(message.encode())

    data = client_socket.recv(1024)

    print('Received message from server: {}'.format(data.decode()))

client_socket.close()

print('Disconnected from server')
