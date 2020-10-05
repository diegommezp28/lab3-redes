import socket
import hashlib
from datetime import datetime
import string

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
video1 = open("./video1.mkv", "rb")


def format_address(s):
    filename = s
    filename = filename.replace(', ', '-')
    filename = filename.replace(' ', '_')
    filename = filename.replace('.', '_')
    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    filename = filename.replace("'", '')
    return filename


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(20)
    conn, addr = s.accept()
    now = datetime.now()
    dt_string = now.strftime("%Y_%M_%d_%H_%M_%S")
    conn_id = format_address(str(addr))
    filename = "log_" + conn_id + "_" + dt_string + ".txt"
    print(filename)
    i = 0
    with conn:
        f = open("log/" + filename, "x")
        print('Connected by', addr)
        conn.send(b'OK')
        while True:
            data = conn.recv(4096)
            if data == b'Listo para recibir':
                hashing = hashlib.new('sha256')
                l = video1.read(4096)
                # print(l)
                while len(l) > 0:
                    conn.send(l)
                    hashing.update(l)
                    i += 1
                    # print(i)
                    l = video1.read(4096)

                conn.send(b'hash')
                hash = hashing.hexdigest()
                print(f'Sent Hash: {hash}')
                conn.send(str.encode(hash))

        conn.close()
    s.close()
    # if not data: break
    # conn.sendall(data)
