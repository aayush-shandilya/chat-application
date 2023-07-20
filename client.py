import socket
import os

HOST = '192.168.55.163'      # The server's IP address
PORT = 8080          # The server's port number

                    # Create a client socket using IPv4 and TCP protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    # Connect to the server using the specified IP and port
client_socket.connect((HOST, PORT))

print('Connected to server')

buffer_size = 1024      # Size of the buffer for sending and receiving data

while True:
                        # Prompt the user to enter a message to send to the server
    message = input('Enter message: ')

    if message == 'Bye':
        print('Good Bye')
        break

    if message == 'send_file':
                        # If the user wants to send a file, prompt for the file path
        file_path = input('Enter file path: ')

                        # Check if the specified file exists
        if not os.path.exists(file_path):
            print('File does not exist')
            continue

                            # Send the file size to the server
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
                            # If the user wants to send a regular message, send it as is
        client_socket.sendall(message.encode())

                            # Receive a response from the server (up to 1024 bytes)
    data = client_socket.recv(1024)

                            # Display the received message from the server
    print('Received message from server: {}'.format(data.decode()))

                            # Close the client socket after the loop ends
client_socket.close()

print('Disconnected from server')
