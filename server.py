import socket
import AES as aes

# import keypad as keypad
import os
from dotenv import load_dotenv, dotenv_values
from modbus_test import get_modbus, set_modbus

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
            command = decrypt_message(command)
            print("Received: ", data, " Command: ", command)
            if command == "GET":
                reply = GET()  # This is an encrypted message (bytes)
            elif command == "GET_MODBUS":
                # m_message = get_modbus(['{"request":"read"}']).decode("utf-8")
                m_message = get_modbus([0, 1, 2, 3])
                m_message = str(m_message)
                reply = enctypt_message(m_message)
            elif command.startswith("SET_MODBUS"):
                try:
                    command_parts = command.split('_')
                    _, _, modbus_number, modbus_value = command_parts
                    modbus_number = int(modbus_number)
                    modbus_value = int(modbus_value)
                    m_message = set_modbus(modbus_number, modbus_value)
                    m_message = str(m_message)
                    reply = enctypt_message(m_message)
                except ValueError:
                    reply = enctypt_message("Invalid modbus number.")
            elif command == "MODBUS_TEST":
                m_message = {"outputs":{"A_in_purge":0.47238958575447976,"B_in_purge":0.084946193242193602,"C_in_purge":0.4426642210033267,"cost":0,"f1_flow":640.46000000000004,"f2_flow":0,"liquid_level":44.153205584977918,"pressure":2701.8466171614818,"product_flow":21.320768684966009,"purge_flow":0},"state":{"f1_valve_pos":100,"f2_valve_pos":0,"product_valve_pos":10.023651483939879,"purge_valve_pos":0}}
                m_message = str(m_message)
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
                print("Data has been sent!")
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
