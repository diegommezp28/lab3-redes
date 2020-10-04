from threading import Thread
from socket import socket
import hashlib

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
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
                        self.conn.send(l)
                        hashing.update(l) 
                        print(i)
                        i += 1
                        l = video1.read(4096)                
                self.conn.send(b'hash')
                hash = hashing.hexdigest()
                print(f'Sent Hash: {hash}')                
                self.conn.send(str.encode(hash))
                rec =self.conn.recv(4096)
                if rec == b'Recibido correctamente' :
                    recibido=False
                else:
                    recibido=True
        


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











