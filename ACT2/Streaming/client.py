import cv2
import numpy as np
import socket
import struct

# Constants
MAX_DGRAM = 2 ** 16

multicast_group1 = ('224.3.29.71', 10000)
multicast_group2 = ('224.3.29.72', 10001)
multicast_group3 = ('224.3.29.73', 10002)


def stream_video(channel):
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    client_socket.bind(('', channel[1]))

    # Tell the operating system to add the socket to
    # the multicast group on all interfaces.
    group = socket.inet_aton(channel[0])
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)

    data = b''
    while True:
        packet, _ = client_socket.recvfrom(MAX_DGRAM)

        if struct.unpack("B", packet[0:1])[0] > 1:
            data += packet[1:]
        else:
            data += packet[1:]
            # Get numpy compressed image from bytes stream
            compress_img = np.frombuffer(data, dtype=np.uint8)
            # decompress de image
            img = cv2.imdecode(compress_img, flags=1)
            # Shows de deccoded frame
            try:
                cv2.imshow('Frame', img)
            except Exception as e:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = b''

    cv2.destroyAllWindows()
    client_socket.close()


def main():
    while True:
        print('Los siguiente son los canales disponibles \n')
        print('1.', multicast_group1)
        print('2.', multicast_group2)
        print('3.', multicast_group3)
        print("\n Digite el número correspondiente al canal o presione 'q' para salir del Streaming ")

        option = str(input()).replace(' ', '')

        if option == '1':
            stream_video(multicast_group1)
        elif option == '2':
            stream_video(multicast_group2)
        elif option == '3':
            stream_video(multicast_group3)
        elif option == 'q':
            break
        else:
            print('Opción inválida. \n')


if __name__ == '__main__':
    main()
