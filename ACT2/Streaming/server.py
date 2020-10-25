from threading import Thread
import socket
import cv2
import struct
import math
import time


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

    def udp_frame(self, img, cont):
        # try:
        img = cv2.resize(img, (600, 400))
        # except Exception as e:
        #    print(str(e))
        compressed_data = cv2.imencode(ext='.jpeg', img=img)[1]
        data = compressed_data.tobytes()
        size = len(data)
        num_of_segments = math.ceil(size / self.MAX_IMAGE_DGRAM)
        start_position = 0

        while num_of_segments:
            end_position = min(size, start_position + self.MAX_IMAGE_DGRAM)
            msg = struct.pack("B", num_of_segments) + \
                data[start_position:end_position]
            self.s.sendto(msg, self.addr)
            start_position = end_position
            num_of_segments -= 1

            if cont == 1:
                print('Type: ', type(compressed_data),
                      'Shape: ', compressed_data.shape)
                print('First packet raw is ', len(data), ' bytes')
                print('\nFirst packet total is', len(msg), 'bytes')


class Server(Thread):

    def __init__(self, multicast_group, stream_file_url):
        Thread.__init__(self)
        self.group = multicast_group
        self.url = stream_file_url

    def create_connection(self) -> socket:
        # Create Datagram Socket (UDP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set the time-to-live for messages to 1 so they do not
        # go past the local network segment.
        ttl = struct.pack('b', 1)
        server_socket.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        return server_socket

    def run(self):
        server_socket = self.create_connection()
        while True:
            fs = FrameSegment(server_socket, self.group)

            vid = cv2.VideoCapture(self.url)
            # Prints width x height of the captured frame.
            print(f'Frame sizes: ({vid.get(3)} x {vid.get(4)})')
            cont = 1

            while vid.isOpened():
                ret, frame = vid.read()
                fs.udp_frame(frame, cont)
                cont = 2
                time.sleep(0.02)

            break


def main():
    multicast_group1 = ('224.3.29.71', 10000)
    multicast_group2 = ('224.3.29.72', 10000)
    multicast_group3 = ('224.3.29.73', 10000)
    video_path1 = '../../TCP/video1.mkv'
    video_path2 = '../../TCP/video2.webm'
    video_path3 = '../../TCP/v1.mp4'

    server1 = Server(multicast_group1, video_path1)
    server1.start()

    server2 = Server(multicast_group2, video_path2)
    server2.start()

    server3 = Server(multicast_group3, video_path3)
    server3.start()


if __name__ == '__main__':
    main()
