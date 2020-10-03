import socket   

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

video1 = open("./video1.mkv", "rb")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    i = 0
    with conn:
        print('Connected by', addr)

        l = video1.read(4096)
        conn.send('OK')
        while True:
            data = conn.recv(4096)
            print('data rcvd')
            while l:
                s.send(l)
                i += 1
                print(i)
                l = video1.read(4096)
            break
        conn.close()
    s.close()
            # if not data: break
            # conn.sendall(data)