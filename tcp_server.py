import socket

server = socket.socket()
server.bind(('0.0.0.0', 5000))
server.listen(1)
conn, addr = server.accept()
data_len = int.from_bytes(conn.recv(8), 'big')
data = b""
while len(data) < data_len:
    data += conn.recv(4096)
conn.close()
with open("received_tcp.txt", "wb") as f:
    f.write(data)
print("TCP ile dosya alındı.")
