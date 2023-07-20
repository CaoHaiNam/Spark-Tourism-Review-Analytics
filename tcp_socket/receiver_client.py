# import socket
# import time

# # Server address and port
# server_address = ('202.134.19.49', 1606)

# # Create a TCP/IP socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the server
# client_socket.connect(server_address)

# while True:
#     # conn, addr = client_socket.accept()
#     # print("Connected by:", addr)

#     # Receive and print data continuously
#     while True:
#         # conn, addr = s.accept()
#         # print("Connected by:", addr) 
#         # 1024 refers to the maximum number of bytes to be received from the TCP socket connection conn.
#         data = client_socket.recv(1024)
#         if not data:
#             break
#         print("Received data:", data.decode())

# # Close the socket (unreachable in this example)
# client_socket.close()

import socket

HOST = '202.134.19.49'  # Replace with the IP address of your server
PORT = 1606

def receive_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received message:", data)

if __name__ == "__main__":
    receive_messages()
