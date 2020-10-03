import socket   

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

video1 = open("./video1.mkv", "rb")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        l = video1.read(4096)
        while True:
            data = conn.recv(1024)

            while l:
                s.send(l)
                l = video1.read(4096)
            break
        conn.close()
    s.close()
            # if not data: break
            # conn.sendall(data)