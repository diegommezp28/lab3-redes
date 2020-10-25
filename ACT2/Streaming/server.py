import socket
import cv2
import struct
import math


class FrameSegment(object):
    """
    This class takes a frame and brakes it down to
    fit the maximum UDP segment size (64KB). It also adds information
    of the packets order for the client to reassemble
    """
    MAX_DGRAM = 2 ** 16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 128  # Image size - 128Bytes pto prevent Overflow

    def __init__(self, scket, address):
        self.s = scket
        self.addr = address

    def udp_frame(self, img):
        img = cv2.resize(img, (600, 400))
        compressed_data = cv2.imencode(ext='.jpeg', img=img)[1]
        data = compressed_data.tobytes()
        size = len(data)
        num_of_segments = math.ceil(size / self.MAX_IMAGE_DGRAM)
        start_position = 0

        while num_of_segments:
            end_position = min(size, start_position + self.MAX_IMAGE_DGRAM)
            msg = struct.pack("B", num_of_segments) + data[start_position:end_position]
            self.s.sendto(msg, self.addr)
            start_position = end_position
            num_of_segments -= 1


# Create Datagram Socket (UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host_ip = "localhost"
port = 8000
socket_address = (host_ip, port)
print('Address: ', socket_address)

buff = 4096

# Socket Bind
server_socket.bind(socket_address)

while True:
    # Receive Hello message from client
    data, addr = server_socket.recvfrom(4096)
    print('GOT CONNECTION FROM:', addr, ' It said: ', data)

    fs = FrameSegment(server_socket, addr)

    if data:
        vid = cv2.VideoCapture('../../TCP/video1.mkv')
        print(f'Frame sizes: ({vid.get(3)} x {vid.get(4)})')  # Prints width x height of the captured frame.
        cont = 1

        while vid.isOpened():
            ret, frame = vid.read()
            fs.udp_frame(frame)
            compressedData = cv2.imencode(ext='.jpeg', img=frame)[1]

            # Prints control info for the first packet sent
            a = compressedData.tobytes()
            message = struct.pack("Q", len(a)) + a
            if cont == 1:
                print('Type: ', type(compressedData), 'Shape: ', compressedData.shape)
                print('First packet is ', len(a), ' bytes')
                cont += 1
    break
