from threading import Thread
import socket
from datetime import datetime
import hashlib
import time

from server_log import log
from server_view import preguntar

HOST = ''  # 'localhost' IP de enlace
PORT = 7735        # Puerto de conección
windowSize = 4
mss = 500


def bytes_of(s):
    return len(s.encode('utf-8'))


class Client(Thread):

    def __init__(self, sock, file_to_send, file_size):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.sock = sock
        self.file_to_send = file_to_send
        self.file_size = file_size
        self.mss = mss
        self.packetList = list()  # Packet List as buffer to save data as the packet to be sent
        self.window_end = windowSize
        self.unacked = 0
        self.total_unacked = 0
        self.timeout = 0.1  # Timeout value for every packet to be sent
        self.sequenceNumber = 0  # default sequence Number to divide file

    # Carry bit used in one's combliment

    def carry_around_add(self, num_1, num_2):
        c = num_1 + num_2
        return (c & 0xffff) + (c >> 16)

    # Calculate the checksum of the data only. Return True or False
    def checksum(self, msg):
        """Compute and return a checksum of the given data"""
        msg = msg.decode('utf-8', errors='ignore')
        if len(msg) % 2:
            msg += "0"

        s = 0
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
            s = self.carry_around_add(s, w)
        return ~s & 0xffff

    def divideFile(self, mss, filename, sequenceNumber):
        #k = list()
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
                checksum = self.checksum(couple_bytes)
                if i + mss > length:
                    # adding eof value = 1 for the lastpacket
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, checksum, 1))
                else:
                    self.packetList.append(
                        Packet(sequenceNumber, couple_bytes, checksum, 0))
                i += mss
                temp = int(sequenceNumber, 2) + 1
                sequenceNumber = format(temp, '032b')
        return self.packetList

    def send():
        sendingData = self.divideFile(
            self.mss, self.file_to_send, self.sequenceNumber)
        self.unacked = 0
        self.total_unacked = 0
        while self.unacked < len(sendingData):
            if self.total_unacked < self.window_end and (self.total_unacked + self.unacked) < len(sendingData):
                for i in sendingData:
                    sq = int(i.sequenceNumber, 2)
                    if sq == self.total_unacked + self.unacked:
                        sendingPkt = i
                self.sock.send(pickle.dumps(sendingPkt))
                self.total_unacked += 1
                continue
            else:
                ready = select.select([self.sock], [], [], self.timeout)
                if ready[0]:
                    ackData, address = self.sock.recvfrom(4096)
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
        benviados = 0  # float(self.file_size)*1000000
        self.conn.send(b'OK')
        benviados += bytes_of('OK')
        data = self.conn.recv(4096)
        if data == b'Listo para recibir':
            print('Esperando...')
            while(faltan != 0):
                continue
            print('Empieza a transmitir')
            send()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.setblocking(0)
    # s.listen(0)
    print('Servidor en: ', HOST, PORT)
    connected = 0
    terminar, num_con, file_to_send, file_size = preguntar()
    print(terminar)
    global faltan
    faltan = 0
    while not terminar:
        c = Client(s, file_to_send, file_size)
    #    while True:
    #        conn, addr = s.accept()
    #        connected += 1
    #        faltan = num_con - connected
    #        c = Client(conn, addr, file_to_send, file_size)
    #        c.start()
    #        print("%s:%d se ha conectado." % addr)
    #        print("Faltan " + str(faltan) + " conexiones")
    print('Apagando')


if __name__ == "__main__":
    main()
