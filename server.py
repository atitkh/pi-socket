import socket
import AES as aes

# import keypad as keypad
import os
from dotenv import load_dotenv, dotenv_values
from modbus_test import get_modbus

load_dotenv()

host = ""
port = 5560
useKeypad = True


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
    key = os.getenv("SECRET_KEY")
    key = key.encode("utf-8")
    cipher = aes.AESCipher(key)
    print("Message: ", message)
    encrypted_message = cipher.encrypt(message)
    print("Encrypted message (Bytes): ", encrypted_message)
    return encrypted_message


def decrypt_message(encrypted_message):
    key = os.getenv("SECRET_KEY")
    key = key.encode("utf-8")
    cipher = aes.AESCipher(key)
    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message: ", decrypted_message)
    return decrypted_message


def GET():
    encrypted_message = enctypt_message("Hello world! Test message 123.")
    return encrypted_message


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
            print("Received: ", data)
            command = decrypt_message(command)
            if command == "GET":
                reply = GET()  # This is an encrypted message (bytes)
            elif command == "MODBUS":
                m_message = get_modbus('{"request":"read"}').decode("utf-8")
                reply = enctypt_message(m_message)
            elif command == "KEYPAD":
                if useKeypad:
                    #     pad = keypad.Keypad()
                    #     keypad_input = pad.readKeypad()
                    #     reply = enctypt_message(keypad_input)
                    # else:
                    reply = enctypt_message("Keypad is disabled.")
            elif command == "KILL":
                print("Server is shutting down.")
                conn.sendall(str.encode("Server shutting down"))
                s.close()
                return False  # Signal to stop the server
            else:
                reply = "Unknown Command"

            # Send reply
            if isinstance(reply, bytes):
                conn.sendall(
                    reply
                )  # If reply is already bytes (like encrypted message), send it directly
            else:
                conn.sendall(
                    str.encode(reply)
                )  # If reply is a string, encode it to bytes first

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
