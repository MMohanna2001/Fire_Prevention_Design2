import socket
import random
import time
# Define the IP address and port to listen on
HOST = '192.168.24.26'  # Pi's IP address
PORT = 6000


    
while True:
    print('Waiting for a connection...')

# Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)    

    try:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print('Connected to:', client_address)

        while True:
            # Generate a random number between 0 and 100
            number = random.randint(0, 100)

            try:
                
                # Send the array to the client
                data = [number, 200, 25.5, 28.7, 1, 1, 0, 1, 0]
                data_str = ','.join(map(str, data))
                client_socket.sendall(data_str.encode())

            except BrokenPipeError:
                print('Client disconnected')
                break

            time.sleep(1)  # Delay between sending data

    finally:
        # Close the client socket
        client_socket.close()

        # Close the server socket
        server_socket.close()


