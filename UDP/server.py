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
windowSize = 1
mss = 3900


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
        self.sequenceNumber = 0  # default sequence Number to divide file
        self.hash = ""
        self.file_size = file_size
        self.file_bytes = 0
        self.file_packs = 0

    def divideFile(self, mss, filename, sequenceNumber):
        #k = list()
        print('Empieza a dividir ' + filename)
        sequenceNumber = format(sequenceNumber, '032b')
        with open(filename, "rb") as binary_file:
            # Read the whole file at once
            data = binary_file.read()
            # Seek position and read N bytes
            i = 0
            # Hashing
            hashing = hashlib.new('sha256')
            length = sys.getsizeof(data)
            while i <= length:
                binary_file.seek(i)  # Go to beginning
                couple_bytes = binary_file.read(mss)
                self.file_bytes += len(couple_bytes)
                self.file_packs += 1
                if i + mss > length:
                    # adding eof value = 1 for the lastpacket
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, 1))
                else:
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, 0))
                hashing.update(couple_bytes)
                i += mss
                temp = int(sequenceNumber, 2) + 1
                sequenceNumber = format(temp, '032b')
            print('Termina de dividir ' + filename)
            self.hash = hashing.hexdigest()
            print(f'Hash calculado: {self.hash}')
        return self.packetList

    def send(self):
        sendingData = self.divideFile(
            self.mss, self.file_to_send, self.sequenceNumber)
        print('Empieza a enviar')
        now = datetime.now()
        start_time = time.time()
        for sendingPkt in sendingData:
            self.sock.sendto(pickle.dumps(sendingPkt), self.address)
        print('Termina de enviar')
        time.sleep(0.03)
        print('Enviando Hash')
        self.sock.sendto(b'HASH', self.address)
        time.sleep(0.03)
        self.sock.sendto(str.encode(self.hash), self.address)

        # Recibir resultado
        data, address = self.sock.recvfrom(mss)
        transfer_time = time.time()
        rec = data
        if rec == b'Recibido correctamente':
            print('Recibido correctamente')
            exitosa = True
        else:
            print('Recibido incorrectamente')
            exitosa = False
        # Recibir info de envio, primero paquetes y después bytes
        data, address = self.sock.recvfrom(mss)
        recibidos = repr(data).replace("b'", '').replace("'", "")
        data, address = self.sock.recvfrom(mss)
        brecibidos = repr(data).replace("b'", '').replace("'", "")

        self.sock.close()

        # Registrar en el log
        logFile = log(self.address, now, exitosa, str(transfer_time-start_time),
                      self.file_to_send, self.file_size, str(self.file_packs), recibidos, str(self.file_bytes), brecibidos)
        print("Registro en el log en el archivo " + logFile)

    def run(self):
        global faltan
        data, address = self.sock.recvfrom(mss)
        self.address = address
        print('Reciví', data)
        # Envía el nombre del archivo
        self.sock.sendto(
            bytes(self.file_to_send, encoding='utf-8'), self.address)
        print('Envie el nombre del archivo')
        while(faltan != 0):
            continue
        self.sock.sendto(b'Empezando a transmitir', self.address)
        print('Inicio')
        self.send()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    # s.setblocking(0)
    #print('Servidor en: ', HOST, PORT)
    connected = 0
    terminar, num_con, file_to_send, file_size = preguntar()
    global faltan
    faltan = num_con
    direcciones = {}
    puertoActual = PORT
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
                puertoActual += 1
                faltan = num_con - connected
                # Crea Socket particular
                s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s2.bind((HOST, puertoActual))
                # Envía el nombre del puerto
                s.sendto(bytes(str(puertoActual), encoding='utf-8'), address)
                c = Client(s2, address, file_to_send, file_size)
                c.start()
                print("%s:%d se ha conectado." % address)
                print("Faltan " + str(faltan) + " conexiones")
    print('Apagando')


if __name__ == "__main__":
    main()
