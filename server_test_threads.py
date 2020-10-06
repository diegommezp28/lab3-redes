from threading import Thread
from socket import socket
import hashlib
import time
import server_log
from server_view import preguntar

HOST = 'localhost'  # IP de enlace
PORT = 50007        # Puerto de conección


class Client(Thread):

    def __init__(self, conn, addr, file_to_send):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.file_to_send = file_to_send

    def run(self):
        global faltan
        i = 0
        self.conn.send(b'OK')
        data = self.conn.recv(4096)
        if data == b'Listo para recibir':
            print('Esperando...')
            while(faltan != 0):
                continue
            print('Emepezando Trasnferencia')
            with open('./'+self.file_to_send, 'rb') as file1:
                hashing = hashlib.new('sha256')
                l = file1.read(4096)
                while len(l) > 0:
                    self.conn.send(l)
                    hashing.update(l)
                    print(i)
                    i += 1
                    l = file1.read(4096)
            time.sleep(0.1)
            self.conn.send(b'hash')
            hash = hashing.hexdigest()
            print(f'Hash enviado: {hash}')
            time.sleep(0.03)
            self.conn.send(str.encode(hash))
            rec = self.conn.recv(4096)
            if rec == b'Recibido correctamente':
                print('Recibido correctamente')
            else:
                print('Recibido incorrectamente')


def main():
    s = socket()

    s.bind((HOST, PORT))
    s.listen(0)
    connected = 0
    terminar, num_con, file_to_send = preguntar()
    global faltan
    if not terminar:
        while True:
            conn, addr = s.accept()
            connected += 1
            faltan = num_con - connected
            c = Client(conn, addr, file_to_send)
            c.start()
            print("%s:%d se ha conectado." % addr)
            print("Faltan " + str(faltan) + " conexiones")
    print('Apagando')


if __name__ == "__main__":
    main()
