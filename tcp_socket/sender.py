import socket
import time

# Server address and port
server_address = ('202.134.19.49', 1606)

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

while True:
    # Data to send
    data = 'Hello, receiver!\n'
    
    # Send data to the server
    client_socket.sendall(data.encode())
    
    # Print the sent data
    print(f"Sent: {data}")
    
    # Sleep for a certain duration before sending the next data
    time.sleep(5)

# Close the socket (unreachable in this example)
client_socket.close()