from threading import Thread
import socket
from datetime import datetime
import hashlib
import time
import sys
from packet import *
import sys
import time
import pickle
import select
import signal
import os
import timeit
import threading


from server_log import log
from server_view import preguntar

HOST = ''  # 'localhost' IP de enlace
PORT = 7735        # Puerto de conección
windowSize = 10
mss = 500


def bytes_of(s):
    return len(s.encode('utf-8'))


class Client(Thread):

    def __init__(self, sock, address, file_to_send, file_size):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.file_to_send = file_to_send
        self.file_size = file_size
        self.mss = mss
        self.packetList = list()  # Packet List as buffer to save data as the packet to be sent
        self.window_end = windowSize
        self.unacked = 0
        self.total_unacked = 0
        self.timeout = 0.1  # Timeout value for every packet to be sent
        self.sequenceNumber = 0  # default sequence Number to divide file

    def divideFile(self, mss, filename, sequenceNumber):
        #k = list()
        print('Empieza a dividir ' + filename)
        sequenceNumber = format(sequenceNumber, '032b')
        with open(filename, "rb") as binary_file:
            # Read the whole file at once
            data = binary_file.read()
            # Seek position and read N bytes
            i = 0
            length = sys.getsizeof(data)
            while i <= length:
                binary_file.seek(i)  # Go to beginning
                couple_bytes = binary_file.read(mss)
                if i + mss > length:
                    # adding eof value = 1 for the lastpacket
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, 1))
                else:
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, 0))
                i += mss
                temp = int(sequenceNumber, 2) + 1
                sequenceNumber = format(temp, '032b')
            print('Termina de dividir ' + filename)
        return self.packetList

    def send(self):
        sendingData = self.divideFile(
            self.mss, self.file_to_send, self.sequenceNumber)
        print('Empieza a enviar')
        self.unacked = 0
        self.total_unacked = 0
        while self.unacked < len(sendingData):
            if self.total_unacked < self.window_end and (self.total_unacked + self.unacked) < len(sendingData):
                print('Caso1')
                for i in sendingData:
                    sq = int(i.sequenceNumber, 2)
                    if sq == self.total_unacked + self.unacked:
                        sendingPkt = i
                self.sock.sendto(pickle.dumps(sendingPkt), self.address)
                self.total_unacked += 1
                continue
            else:
                print('Caso2')
                ready = select.select([self.sock], [], [], self.timeout)
                if ready[0]:
                    ackData, address = self.sock.recvfrom(4096)
                    if(address == self.address):
                        ackData = pickle.loads(ackData)
                        if ackData.ackField != 0b1010101010101010:
                            continue
                        if int(ackData.sequenceNumber, 2) == self.unacked:
                            self.unacked += 1
                            self.total_unacked -= 1
                        else:
                            self.total_unacked = 0
                            continue
                else:
                    print('Timeout, sequence number = ', self.unacked)
                    self.total_unacked = 0
                    continue

        print('Files are transmitted successfully.')
        self.sock.close()

    def run(self):
        global faltan
        i = 0
        benviados = 0
        # Envía el nombre del archivo
        self.sock.sendto(
            bytes(self.file_to_send, encoding='utf-8'), self.address)
        while(faltan != 0):
            continue
        self.sock.sendto(b'Empezando a transmitir', self.address)
        print('Empieza a transmitir')
        self.send()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    # s.setblocking(0)
    print('Servidor en: ', HOST, PORT)
    connected = 0
    terminar, num_con, file_to_send, file_size = preguntar()
    global faltan
    faltan = num_con
    direcciones = {}
    if not terminar:
        while faltan != 0:
            print('Esperando...')
            data, address = s.recvfrom(mss)
            dir_pu = address[0]+str(address[1])
            ya_conectado = False if not direcciones.get(
                dir_pu, False) else True
            if(data == b'Hola servidor' and not ya_conectado):
                direcciones[dir_pu] = True
                connected += 1
                faltan = num_con - connected
                c = Client(s, address, file_to_send, file_size)
                c.start()
                print("%s:%d se ha conectado." % address)
                print("Faltan " + str(faltan) + " conexiones")
    print('Apagando')


if __name__ == "__main__":
    main()
