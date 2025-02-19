import socket
from pymodbus.client import ModbusTcpClient

# OpenPLC IP address and port
plc_ip = 'cci-pc.ddns.ualr.edu'
plc_port = 502

def get_socket(message):
    # socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port to connect
    port = 55555
    
    s.connect((plc_ip, port))
    # send a message to the server
    s.send(message.encode())
    # receive data from the server
    message = s.recv(1024)
    # close the connection
    s.close()
    return message

def get_modbus(index):
    try:
        # Connect to OpenPLC
        client = ModbusTcpClient(plc_ip, port=plc_port)
        client.connect()

        # Read from output register
        results = []
        for address in index:
            result = client.read_coils(address)

            # Check if the read was successful
            if not result.isError():
                coil_status = result.bits[0]
                results.append(coil_status)
            else:
                print(f"Error reading coil: {result}")
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close connection
        client.close()
