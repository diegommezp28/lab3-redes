import cv2
import numpy as np
import socket
import struct

# Constant
MAX_DGRAM = 2 ** 16

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = 'localhost'  # Put the server's ip address here
port = 8000  # Put the server's listening port here
server_address = (host_ip, port)

data = b""
message = b'Hello.'

client_socket.sendto(message, server_address)

while True:
    packet, _ = client_socket.recvfrom(MAX_DGRAM)
    # print('Packet number: ', struct.unpack("B", packet[0:1])[0])
    if struct.unpack("B", packet[0:1])[0] > 1:
        data += packet[1:]
    else:
        data += packet[1:]
        compress_img = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(compress_img, flags=1)
        cv2.imshow('Frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        data = b''

cv2.destroyAllWindows()
client_socket.close()
