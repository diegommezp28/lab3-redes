import socket
import hashlib

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
        conn.send(b'OK')
        while True:
            data = conn.recv(4096)
            print(data)
            if data==b'Listo para recibir':
                hashing = hashlib.new('sha256')
                
                l = video1.read(4096)
                print(l)
                while len(l)>0:
                    conn.send(l)
                    hashing.update(l) 
                    i += 1
                    l = video1.read(4096)                
                
                
                conn.send(b'hash')
                hash = hashing.hexdigest()
                print(f'Sent Hash: {hash}')                
                conn.send(str.encode(hash))
                
        conn.close()
    s.close()
            # if not data: break
            # conn.sendall(data)
