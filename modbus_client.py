# from pymodbus.client import AsyncModbusTcpClient

from pymodbus.client import ModbusTcpClient
# import json

# class ModbusClient:
#     def __init__(self, host, port):
#         # Create a Modbus TCP client instance
#         self.client = AsyncModbusTcpClient(host)

#     def connect(self):
#         if self.client.connect():
#             print("Connected to Modbus server.")
#             return True
#         else:
#             print("Failed to connect to Modbus server.")
#             return False

#     def read_register(self, address):
#         # Read a holding register
#         response = self.client.read_holding_registers(address, 1)
#         if response.isError():
#             print("Error reading register:", response)
#             return None
#         else:
#             return response.registers[0]

#     def close(self):
#         self.client.close()
#         print("Connection closed.")


# OpenPLC IP address and port
plc_ip = '127.0.0.1'  # Replace with your OpenPLC's IP
plc_port = 502

# Modbus addresses (adjust based on your OpenPLC mapping)
input_register = 0
output_register = 1
holding_register = 40001

# Values to write
input_value = 1
output_value = 0

try:
    # Connect to OpenPLC
    client = ModbusTcpClient(plc_ip, port=plc_port)
    client.connect()

    # Write to input register
    # client.write_register(input_register, input_value)
    # print(f"Wrote {input_value} to input register {input_register}")

    # Read from output register
    result = client.read_holding_registers(address=output_register, count=1)
    if not result.isError():
        output_read_value = result.registers[0]
        print(f"Read {output_read_value} from output register {output_register}")
    else:
        print(f"Error reading output register: {result}")

    # Write to holding register
        # client.write_register(holding_register, 1234)
        # print(f"Wrote {1234} to holding register {holding_register}")

    # Read from holding register
    read_holding_result = client.read_holding_registers(address=holding_register, count=1)
    if not read_holding_result.isError():
        holding_register_value = read_holding_result.registers[0]
        print(f"Read {holding_register_value} from holding register {holding_register}")
    else:
        print(f"Error reading holding register: {read_holding_result}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close connection
    client.close()