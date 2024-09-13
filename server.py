import socket
import AES as aes
from Crypto.Random import get_random_bytes

host = ""
port = 5560

def setupSocketServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
        s.close()
        return None
    print("Socket binded.")
    return s


def setupConnection(s):
    s.listen(10)
    client_conn, address = s.accept()
    print(address[0] + ":" + str(address[1]) + " has connected.")
    return client_conn

def enctypt_message(message):
    key = "UASecretPassword"
    key = key.encode('utf-8')
    cipher = aes.AESCipher(key)
    encrypted_message = cipher.encrypt(message)
    print("Encrypted message (Bytes): ", encrypted_message)
    return encrypted_message

def GET():
    encrypted_message = enctypt_message("Hello World. What is UP? You GOodD?")
    return encrypted_message


def REPEAT(dataMessage):
    return dataMessage[1] if len(dataMessage) > 1 else "No data provided"


def dataTransfer(conn):
    conn.settimeout(60)  # Set a timeout for client connection
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode("utf-8")
            dataMessage = data.split(" ", 1)
            command = dataMessage[0]
            print("Command: ", command)
            if command == "GET":
                reply = GET()  # This is an encrypted message (bytes)
            elif command == "REPEAT":
                reply = REPEAT(dataMessage)  # This is a string
            elif command == "KILL":
                print("Server is shutting down.")
                conn.sendall(str.encode("Server shutting down"))
                s.close()
                return False  # Signal to stop the server
            else:
                reply = "Unknown Command"

            # Send reply
            if isinstance(reply, bytes):
                conn.sendall(reply)  # If reply is already bytes (like encrypted message), send it directly
            else:
                conn.sendall(str.encode(reply))  # If reply is a string, encode it to bytes first

            print("Data has been sent!")
    except socket.timeout:
        print("Connection timed out.")
    except socket.error as e:
        print("Socket error: ", e)
    finally:
        conn.close()
    return True  # Keep the server running


s = setupSocketServer()
if s:
    while True:
        try:
            conn = setupConnection(s)
            if not dataTransfer(conn):
                break
        except Exception as e:
            print("Server error:", e)