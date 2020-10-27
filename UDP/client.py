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

HOST = '192.168.2.133'  # 'localhost'    # The remote host
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
        # Iniciar comunicación con el servidor
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

        # Crea directorios
        data, address = self.sock.recvfrom(bufsize)
        filepath = folder+'/'+str(newPORT)+'/'
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
        # Empieza a recibir
        print('Empezando recepción')
        hash = ''
        brecibidos = 0
        paquetes_recibidos = 0
        try:
            while True:
                try:
                    data_raw, address = self.sock.recvfrom(bufsize)
                    if data_raw == b'HASH':
                        data_raw, address = self.sock.recvfrom(bufsize)
                        hash = data_raw
                        break
                    else:
                        data = pickle.loads(data_raw)
                        brecibidos += len(data.packet)
                        paquetes_recibidos += 1

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

            # Revisar el hash recibido y el enviado
            hasher = hashlib.new('sha256')
            with open(filepath+file_sended, 'rb') as archivo:
                buffer = archivo.read(3900)
                while len(buffer) > 0:
                    hasher.update(buffer)
                    buffer = archivo.read(3900)
            hashC = hasher.hexdigest()
            print(
                f'Hash recibido: {hash.decode()} y Hash Calculado: {hashC}')
            # Veredicto
            if hashC == hash.decode():
                self.sock.send(b'Recibido correctamente')
                print('Recibido correctamente')
            else:
                self.sock.send(b'Recibido incorrectamente')
                print('Recibido incorrectamente')

            # Cantidad de paquetes recibidos y bytes recibidos
            self.sock.send(bytes(str(paquetes_recibidos),  encoding='utf-8'))
            self.sock.send(bytes(str(brecibidos),  encoding='utf-8'))

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
