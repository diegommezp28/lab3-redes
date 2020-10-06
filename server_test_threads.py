from threading import Thread
from socket import socket
import hashlib
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port


class Client(Thread):
        
    def __init__(self, conn, addr):
        # Inicializar clase padre.
        Thread.__init__(self)        
        self.conn = conn
        self.addr = addr
    
    def run(self):
        i=0
        self.conn.send(b'OK')        
        data = self.conn.recv(4096)
        if data==b'Listo para recibir':
            recibido = True
            while recibido:
                with open('./video1.mkv', 'rb') as video1:
                    hashing = hashlib.new('sha256')                
                    l = video1.read(4096)
                    while len(l)>0:
                        self.conn.sendall(l)
                        hashing.update(l) 
                        print(i)
                        i += 1
                        l = video1.read(4096)

                time.sleep(0.1)
                self.conn.sendall(b'hash')
                hash = hashing.hexdigest()
                print(f'Sent Hash: {hash}')
                time.sleep(0.03)
                self.conn.sendall(str.encode(hash))
                rec =self.conn.recv(4096)

                if rec == b'Recibido correctamente' :
                    recibido=False
                else:
                    recibido=True

                break
        self.conn.close()


def main():
    s = socket()

    # Escuchar peticiones en el puerto 6030.
    s.bind((HOST, PORT))
    s.listen(0)
    
    while True:
        conn, addr = s.accept()
        c = Client(conn, addr)
        c.start()
        print("%s:%d se ha conectado." %addr)


if __name__ == "__main__":
    main()











