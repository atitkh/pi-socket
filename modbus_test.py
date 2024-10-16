import socket

def get_modbus(message):
    # socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port to connect
    port = 55555
    
    s.connect(('192.168.95.10', port))
    # send a message to the server
    s.send(message.encode())
    # receive data from the server
    message = s.recv(1024)
    # close the connection
    s.close()
    return message
