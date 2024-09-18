from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class AESCipher:
    def __init__(self, key: bytes):
        # key length 16 bytes for AES-128
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

    def decrypt(self, data: str) -> str:
        # Base64 decode the input data to get the combined IV + ciphertext
        data_bytes = base64.b64decode(data)

        # Extract the first 16 bytes (IV) and the rest (encrypted data)
        iv = data_bytes[:AES.block_size]
        encrypted_data = data_bytes[AES.block_size:]

        # AES cipher object for decryption
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)

        # Decrypt and unpad the plaintext data
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        return decrypted_data.decode('utf-8')