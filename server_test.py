import socket
from hashlib import sha256

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
hashing = sha256()
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

            l = video1.read(4096)
            while l:
                conn.send(l)
                hashing.update(l)
                i += 1
                print(i)
                l = video1.read(4096)
            break

        conn.send(b'hash')

        hash = hashing.hexdigest()
        conn.send(str.encode(hash))

        print(f'Sent Hash: {hash}')

        conn.close()
    s.close()
            # if not data: break
            # conn.sendall(data)
