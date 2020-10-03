# Echo client program
import socket
from hashlib import sha256

HOST = '192.168.1.133'    # The remote host
PORT = 50007  # The same port as used by the server

video1 = open("./save_content/video1.mkv", "wb")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(4096)
    print('Received', repr(data))

    s.sendall(b'Hello, world')

    i = 0
    while True:
        l = s.recv(4096)
        i+=1
        print(l)
        while l:
            video1.write(l)
            l = s.recv(4096)
            i += 1
            print(i)

            if l == b'hash':
                break

        hash = s.recv(4096)
        print(hash)

        break
    s.close()

# with open("./save_content/video1.mkv", "rb") as video:
#     hashing = sha256()
#     hashing.update(video)
#     hash = hashing.hexdigest()
#
#     print('what i got')
#     print(hash)
