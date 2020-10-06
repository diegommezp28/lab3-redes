from threading import Thread
from socket import socket
from datetime import datetime
import hashlib
import time

from server_log import log
from server_view import preguntar

HOST = 'localhost'  # IP de enlace
PORT = 50007        # Puerto de conección


def bytes_of(s):
    return len(s.encode('utf-8'))


class Client(Thread):

    def __init__(self, conn, addr, file_to_send, file_size):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.file_to_send = file_to_send
        self.file_size = file_size

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
            now = datetime.now()
            print('Enviando nombre archivo')
            self.conn.sendall(bytes(self.file_to_send, encoding='utf-8'))
            benviados += bytes_of(self.file_to_send)
            time.sleep(0.1)
            self.conn.sendall(b'Emepezando Transferencia')
            benviados += bytes_of('Emepezando Transferencia')
            time.sleep(0.1)
            print('Emepezando Transferencia')
            start_time = time.time()
            with open('./'+self.file_to_send, 'rb') as file1:
                hashing = hashlib.new('sha256')
                l = file1.read(4096)
                while len(l) > 0:
                    self.conn.send(l)
                    benviados += len(l)
                    hashing.update(l)
                    # print(i)
                    i += 1
                    l = file1.read(4096)
            time.sleep(0.1)
            self.conn.send(b'hash')
            benviados += bytes_of('hash')
            hash = hashing.hexdigest()
            print(f'Hash enviado: {hash}')
            time.sleep(0.03)
            self.conn.send(str.encode(hash))
            benviados += 32  # bytes_of(str.encode(hash))
            transfer_time = time.time()
            rec = self.conn.recv(4096)
            # if rec == b'Cantidad Paquetes':
            #    print('Cantidad de paquetes bien recibida')
            rec = self.conn.recv(4096)
            recibidos = repr(rec).replace("b'", '').replace("'", "")
            rec = self.conn.recv(4096)
            # if rec == b'Cantidad bytes':
            #    print('Cantidad de bytes bien recibida')
            rec = self.conn.recv(4096)
            brecibidos = repr(rec).replace("b'", '').replace("'", "")
            #print('Cantidad de bytes recibidos:', brecibidos)
            rec = self.conn.recv(4096)
            if rec == b'Recibido correctamente':
                print('Recibido correctamente')
                exitosa = True
            else:
                print('Recibido incorrectamente')
                exitosa = False
            logFile = log(self.addr, now, exitosa, str(transfer_time-start_time),
                          self.file_to_send, self.file_size, str(i), recibidos, str(benviados), brecibidos)
            print("Registro en el log en el archivo " + logFile)


def main():
    s = socket()

    s.bind((HOST, PORT))
    s.listen(0)
    connected = 0
    terminar, num_con, file_to_send, file_size = preguntar()
    global faltan
    if not terminar:
        while True:
            conn, addr = s.accept()
            connected += 1
            faltan = num_con - connected
            c = Client(conn, addr, file_to_send, file_size)
            c.start()
            print("%s:%d se ha conectado." % addr)
            print("Faltan " + str(faltan) + " conexiones")
    print('Apagando')


if __name__ == "__main__":
    main()
