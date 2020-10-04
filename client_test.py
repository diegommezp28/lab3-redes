# Echo client program
import socket
import hashlib

HOST = '192.168.1.133'    # The remote host
PORT = 50007  # The same port as used by the server





with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(4096)
    print('Received', repr(data))

    s.sendall(b'Listo para recibir')

    i = 0
    recibido=True
    while recibido:
        with open('./save_content/video1.mkv', 'wb') as video1:
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

        hasher = hashlib.new('sha256')
        with open('./save_content/video1.mkv', 'rb') as video:
            buffer = video.read(4096)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = video.read(4096)
        hashC=hasher.hexdigest()
        print(f'Received Hash: {hash.decode()} and Calculated Hash: {hashC}')
        if hashC==hash.decode():
            s.sendall(b'Recibido correctamente')
            recibido=False
        else:
            s.sendall(b'Recibido incorrectamente')



        break
    
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