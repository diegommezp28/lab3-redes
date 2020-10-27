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
import os
import errno

from packet import *

HOST = 'localhost'  # '192.168.2.133'    # The remote host
PORT = 7735  # The same port as used by the server
folder = './save_content/'
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
        # Recibe el nuevo puerto
        data, address = self.sock.recvfrom(bufsize)
        newPORT = int(repr(data).replace("b'", '').replace("'", ""))
        print('Nuevo puerto: ', newPORT)
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((HOST, newPORT))
        self.sock.send(bytes('Hola servidor, me conecte a ' +
                             str(newPORT),  encoding='utf-8'))

        # Recibe el nombre del archivo
        print('Esperando nombre archivo')
        data, address = self.sock.recvfrom(bufsize)
        file_sended = repr(data).replace("b'", '').replace("'", "")
        print('Esperando archivo ', file_sended)

        data, address = self.sock.recvfrom(bufsize)
        filepath = './save_content/'+str(newPORT)+'/'
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        file = open(filepath+file_sended, 'wb')
        i = 0
        while(data != b'Empezando a transmitir'):
            continue
        print('Empezando recepción')
        try:
            while True:
                try:
                    data, address = self.sock.recvfrom(bufsize)
                    data = pickle.loads(data)

                except socket.error:
                    continue
                except KeyboardInterrupt:
                    self.sock.close()
                    sys.exit(0)

                file.write(data.packet)
                if data.eof == 1:
                    print('File Received.')
                    sys.exit(0)
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
