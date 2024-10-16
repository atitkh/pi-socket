from pymodbus.client import AsyncModbusTcpClient
import json

class ModbusClient:
    def __init__(self, host, port):
        # Create a Modbus TCP client instance
        self.client = AsyncModbusTcpClient(host)

    def connect(self):
        if self.client.connect():
            print("Connected to Modbus server.")
            return True
        else:
            print("Failed to connect to Modbus server.")
            return False

    def read_register(self, address):
        # Read a holding register
        response = self.client.read_holding_registers(address, 1)
        if response.isError():
            print("Error reading register:", response)
            return None
        else:
            return response.registers[0]

    def close(self):
        self.client.close()
        print("Connection closed.")
