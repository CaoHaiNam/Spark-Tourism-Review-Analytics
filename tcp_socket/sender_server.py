import socket
import time
import random

# Server address and port
server_address = ('202.134.19.49', 1606)

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(server_address)
client_socket.listen(1)
conn, addr = client_socket.accept()  

data = 'Hello, receiver!\n'
while True:
    # conn, addr = client_socket.accept()  
    conn.sendall(data.encode()) 
    # Print the sent data
    print(f"Sent: {data}")                               
    time.sleep(random.choice([1,2,3,4]))
    # conn.close()













# import socket
# import time
# import random
# # Create a TCP socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to a specific address and port
# host = '202.134.19.49'  # Change this to the desired host address
# port = 1606  # Change this to the desired port number
# client_socket.bind((host, port))

# # Listen for incoming connections
# client_socket.listen(1)
# data = 'Hello, receiver!\n'
# # Accept a client connection
# while True:
#     conn, addr = client_socket.accept()
#     print("Connected by:", addr)
#     conn, addr = client_socket.accept()  
#     conn.sendall(data.encode()) 
#     # Print the sent data
#     print(f"Sent: {data}")                               
#     time.sleep(random.choice([1,2,3,4]))
#     # conn.close()

#     # Close the connection
#     # print("Connection closed.")
# client_socket.close()

# import socket
# import time
# import random

# # Server address and port
# server_address = ('202.134.19.49', 1606)

# # Create a TCP/IP socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # conn, addr = client_socket.accept()  
# # data = 'Hello, receiver!\nHello, receiver!\nHello, receiver!\nHello, receiver!\nHello, receiver!\n'
# data = 'Hello, receiver!\n'
# client_socket.bind(server_address)
# client_socket.listen(1)
# # conn, addr = client_socket.accept() 
# # while True:
# conn, addr = client_socket.accept()
# while True:  
#     conn.sendall(data.encode()) 
#     # Print the sent data
#     print(f"Sent: {data}")                               
#     time.sleep(random.choice([1,2,3,4]))
# conn.close()
# client_socket.close()



