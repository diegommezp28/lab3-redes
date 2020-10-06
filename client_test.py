# Echo client program
import socket
import hashlib
import time

HOST = 'localhost'  # '192.168.1.133'    # The remote host
PORT = 50007  # The same port as used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(4096)
    if data == b'OK':
        recibido = True
        print('Recibí', repr(data))
        s.sendall(b'Listo para recibir')
        data = s.recv(4096)
        file_sended = repr(data).replace("b'", '').replace("'", "")
        print('Nombre archivo', file_sended)
        data = s.recv(4096)
        if data == b'Emepezando Trasnferencia':
            print('Bien')
        paquetes = 0
        if recibido:
            with open('./save_content/'+file_sended, 'wb') as archivo:
                l = s.recv(4096)
                i = 1
                # print(l)
                while l:
                    archivo.write(l)

                    l = s.recv(4096)

                    i += 1

                    # print(i)
                    if l == b'hash':
                        print('Hash flag')
                        break
            hash = s.recv(4096)
            s.sendall(b'Cantidad Paquetes')
            time.sleep(0.1)
            s.sendall(bytes(str(i), encoding='utf-8'))
            time.sleep(0.1)
            hasher = hashlib.new('sha256')
            with open('./save_content/'+file_sended, 'rb') as archivo:
                buffer = archivo.read(4096)
                while len(buffer) > 0:
                    hasher.update(buffer)
                    buffer = archivo.read(4096)
            hashC = hasher.hexdigest()
            print(
                f'Hash recibido: {hash.decode()} y Hash Calculado: {hashC}')
            time.sleep(0.1)

            if hashC == hash.decode():
                s.sendall(b'Recibido correctamente')
                print('Recibido correctamente')
            else:
                s.sendall(b'Recibido incorrectamente')
            s.sendall(b'Paquetes recibidos')
    s.close()
#
# with open("./save_content/video1.mkv", "rb") as video:
#     hashing = sha256()
#
#     l = video.read(4096)  # Read from the file. Take in the amount declared above
#     while l:  # While there is still data being read from the file
#         hashing.update(l)  # Update the hash
#         l = video.read(4096)
#     hash = hashing.hexdigest()
#     hash = str.encode(hash)
#     print(f'Calculated Hash: {hash}')
