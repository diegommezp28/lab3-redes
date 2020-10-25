import cv2
import numpy as np
import socket
import struct

# Constant
MAX_DGRAM = 2 ** 16

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
client_socket.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
client_socket.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

# host_ip = 'localhost'  # Put the server's ip address here
# port = 8000  # Put the server's listening port here
# server_address = (host_ip, port)

# data = b""
# message = b'Hello.'
#
# client_socket.sendto(message, server_address)

print('\nwaiting to receive message')
data, address = client_socket.recvfrom(1024)
print('Data received', data)

print('sending acknowledgement to', address)
client_socket.sendto(b'ack', address)

data = b''
while True:
    packet, _ = client_socket.recvfrom(MAX_DGRAM)
    # print('Packet number: ', struct.unpack("B", packet[0:1])[0])
    if struct.unpack("B", packet[0:1])[0] > 1:
        data += packet[1:]
    else:
        data += packet[1:]
        compress_img = np.frombuffer(data, dtype=np.uint8)
        # print(compress_img.shape)
        img = cv2.imdecode(compress_img, flags=1)
        # print(img.shape)
        cv2.imshow('Frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        data = b''

cv2.destroyAllWindows()
client_socket.close()
