import socket
import hashlib
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
video1 = open("./video1.mkv", "rb")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(20)
    conn, addr = s.accept()

    i = 0
    with conn:
        print('Connected by', addr)
        conn.sendall(b'OK')
        while True:
            data = conn.recv(4096)
            if data==b'Listo para recibir':
                hashing = hashlib.new('sha256')
                l = video1.read(4096)
                print(l)
                while len(l)>0:
                    conn.sendall(l)
                    hashing.update(l) 
                    i += 1
                    print(i)
                    l = video1.read(4096)                
                
                time.sleep(0.1)
                conn.sendall(b'hash')
                hash = hashing.hexdigest()
                print(f'Sent Hash: {hash}')
                time.sleep(0.03)                
                conn.sendall(str.encode(hash))
                
        conn.close()
    s.close()
            # if not data: break
            # conn.sendall(data)
