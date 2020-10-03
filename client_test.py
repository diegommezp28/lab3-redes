# Echo client program
import socket

HOST = '192.168.1.133'    # The remote host
PORT = 50007  # The same port as used by the server

video1 = open("./save_content/video1.mkv", "a+")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(4096)
    print('Received', repr(data))

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
        break
    s.close()