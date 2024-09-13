from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


class AESCipher:
    def __init__(self, key: bytes):
        # Ensure the key is of length 16 bytes for AES-128, 24 bytes for AES-192, or 32 bytes for AES-256
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes long.")
        self.key = key
        # print("Key (Base64): ", base64.b64encode(key).decode("utf-8"))

    def encrypt(self, data: str) -> str:
        data_bytes = data.encode("utf-8")
        padded_data = pad(data_bytes, AES.block_size)

        # AES cipher object and encrypt data
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(padded_data)

        # debugging
        print("IV (base64): ", base64.b64encode(iv).decode("utf-8"))
        print("Data (base64): ", base64.b64encode(encrypted_data).decode("utf-8"))

        # Combine, encode to base64, and send
        combined_data = iv + encrypted_data
        encoded_data = base64.b64encode(combined_data).decode("utf-8")

        return encoded_data
