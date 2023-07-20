import socket

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = '202.134.19.49'  # Change this to the desired host address
port = 1606  # Change this to the desired port number
s.bind((host, port))

# Listen for incoming connections
s.listen(1)

print("Receiver is ready to receive data.")

# Accept a client connection
while True:
    conn, addr = s.accept()
    print("Connected by:", addr)

    # Receive and print data continuously
    while True:
        # conn, addr = s.accept()
        # print("Connected by:", addr) 
        # 1024 refers to the maximum number of bytes to be received from the TCP socket connection conn.
        data = conn.recv(1024)
        if not data:
            break
        print("Received data:", data.decode())

    # Close the connection
    conn.close()
    print("Connection closed.")