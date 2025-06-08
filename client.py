
import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Load server's public RSA key
with open("server_public.pem", "rb") as key_file:
    server_public_key = serialization.load_pem_public_key(key_file.read())

# Generate AES key
aes_key = os.urandom(32)
iv = os.urandom(16)

# Encrypt AES key with RSA
encrypted_key = server_public_key.encrypt(
    aes_key,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# Encrypt file
filename = "testfile.txt"
with open(filename, "rb") as f:
    data = f.read()

cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(data) + encryptor.finalize()

# Create socket and send data
s = socket.socket()
s.connect(("localhost", 5000))
s.sendall(len(encrypted_key).to_bytes(4, 'big') + encrypted_key)
s.sendall(iv)
s.sendall(len(encrypted_data).to_bytes(8, 'big') + encrypted_data)
s.close()
