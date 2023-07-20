import socket
import threading
import os

HOST = '192.168.55.163'  # The server's IP address
PORT = 8080  # The server's port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print('Server is listening on port {}'.format(PORT))

clients = []

def handle_client(client_socket):
    global clients

    while True:
        data = client_socket.recv(1024)

        if data == b'Bye':
            break

        if data.decode() == 'send_file':
            filename = input('Enter filename: ')

            if not os.path.exists(filename):
                print('File does not exist')
                continue

            with open(filename, 'rb') as f:
                data = f.read()

            client_socket.sendall(data)
        else:
            for client in clients:
                if client != client_socket:
                    client.sendall(data)

    client_socket.close()

while True:
    client_socket, client_address = server.accept()

    print('Client connected from {}'.format(client_address))

    clients.append(client_socket)

    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
