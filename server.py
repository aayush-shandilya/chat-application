import socket
import threading
import os

HOST = '192.168.55.163'  # The server's IP address
PORT = 8080  # The server's port number

        # Create a server socket using IPv4 and TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the server socket to the specified IP and port
server.bind((HOST, PORT))

        # Listen for incoming connections, allowing up to 5 queued connections
server.listen(5)

print('Server is listening on port {}'.format(PORT))

        # List to keep track of connected client sockets
clients = []

def handle_client(client_socket):
    global clients

    while True:
                # Receive data from the client (up to 1024 bytes)
        data = client_socket.recv(1024)

                # If the client sends 'Bye', close the connection
        if data == b'Bye':
            break

                # If the client sends 'send_file', prompt for filename and send the file
        if data.decode() == 'send_file':
            filename = input('Enter filename: ')

            if not os.path.exists(filename):
                print('File does not exist')
                continue

                    # Read the file data and send it to the client
            with open(filename, 'rb') as f:
                data = f.read()

            client_socket.sendall(data)
        else:
                    # If the client sends a regular message, broadcast it to all clients
            for client in clients:
                if client != client_socket:
                    client.sendall(data)

                    # Close the client socket after the loop ends (when 'Bye' is received)
    client_socket.close()

while True:
                    # Accept incoming connection from a client
    client_socket, client_address = server.accept()

    print('Client connected from {}'.format(client_address))

                    # Add the client socket to the list of connected clients
    clients.append(client_socket)

                    # Create a new thread to handle communication with the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
