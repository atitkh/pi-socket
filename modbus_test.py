import socket

# connect to a tcp socket server and send one message
def get_modbus(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the port on which you want to connect
    port = 55555
    # connect to the server on local computer
    s.connect(('192.168.95.10', port))
    # send a message to the server
    s.send(message.encode())
    # receive data from the server
    message = s.recv(1024)
    # close the connection
    s.close()
    return message
