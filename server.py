
import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load server private RSA key
with open("server_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

# Start server
server = socket.socket()
server.bind(("localhost", 5000))
server.listen(1)
conn, addr = server.accept()

# Receive encrypted AES key
key_len = int.from_bytes(conn.recv(4), 'big')
encrypted_key = conn.recv(key_len)

# Receive IV
iv = conn.recv(16)

# Receive encrypted file data
data_len = int.from_bytes(conn.recv(8), 'big')
encrypted_data = b""
while len(encrypted_data) < data_len:
    encrypted_data += conn.recv(4096)

conn.close()

# Decrypt AES key
aes_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# Decrypt data
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

# Save to file
with open("received_testfile.txt", "wb") as f:
    f.write(decrypted_data)
