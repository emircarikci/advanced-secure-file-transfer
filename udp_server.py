import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 6000))
received_data = b""
while True:
    packet, addr = server.recvfrom(1024)
    if packet == b'__END__':
        break
    received_data += packet
with open("received_udp.txt", "wb") as f:
    f.write(received_data)
print("UDP ile dosya alındı.")
