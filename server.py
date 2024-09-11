import socket
import time

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


def GET():
    return "asd test"


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
            if command == "GET":
                reply = GET()
            elif command == "REPEAT":
                reply = REPEAT(dataMessage)
            elif command == "KILL":
                print("Server is shutting down.")
                conn.sendall(str.encode("Server shutting down"))
                s.close()
                return False  # Signal to stop the server
            else:
                reply = "Unknown Command"
            conn.sendall(str.encode(reply))
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