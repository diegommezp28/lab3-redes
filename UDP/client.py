# Echo client program
import hashlib
import sys
import time
import datetime
import socket
import pickle
import select
import signal
import os
import timeit
import threading

from packet import *

HOST = 'localhost'  # '192.168.2.133'    # The remote host
PORT = 7735  # The same port as used by the server
folder = './save_content/'
file_sended = 'video1.mkv'
bufsize = 4096


def bytes_of(s):
    return len(s.encode('utf-8'))


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((HOST, PORT))
        # self.sock.setblocking(0)
        self.expected_seq = 0
        self.ack_seq = 0
        self.timeout = 0.1
        self.packet_loss = False

    def receive(self):
        print("Soy un cliente")
        global data
        self.sock.send(b'Hola servidor')
        print('Esperando...')
        data, address = self.sock.recvfrom(bufsize)
        file = open('./save_content/'+file_sended, 'wb')
        i = 0
        while(data != b'Empezando a transmitir'):
            continue
        print('Empezando recepción')
        try:
            while True:
                try:
                    data, address = self.sock.recvfrom(bufsize)
                    data = pickle.loads(data)
                    if self.expected_seq != int(data.sequenceNumber, 2):
                        continue

                except socket.error:
                    continue
                except KeyboardInterrupt:
                    self.sock.close()
                    sys.exit(0)

                file.write(data.packet)
                sendACK = Acknowledgment(data.sequenceNumber)
                self.sock.send(pickle.dumps(sendACK))
                if data.eof == 1:
                    print('File Received.')
                    sys.exit(0)
                self.expected_seq += 1
            file.close()
        except Exception as e:
            print('Exception', e)
            pass


def main():
    # Arguments are passed in order of acceptance in the command line arguments
    client = Client()
    # try:
    client.receive()
    #print("Run Time:", timeit.timeit(client.receive(), number=1))
    # except:
    #   print("Error occured while sending")


if __name__ == "__main__":
    main()
