import socket
import hashlib
from datetime import datetime
import time
import string
import select

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
fileToSend = "video1.mkv"
video1 = open("./"+fileToSend, "rb")


def format_filename(s, now):
    conn_id = s
    conn_id = conn_id.replace(', ', '-')
    conn_id = conn_id.replace(' ', '_')
    conn_id = conn_id.replace('.', '_')
    conn_id = conn_id.replace('(', '')
    conn_id = conn_id.replace(')', '')
    conn_id = conn_id.replace("'", '')
    dt_string = now.strftime("%Y_%M_%d_%H_%M_%S")
    filename = "log_" + conn_id + "_" + dt_string + ".txt"
    return filename


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    s.bind((HOST, PORT))
    s.listen(20)
    conn, addr = s.accept()
    now = datetime.now()
    filename = format_filename(str(addr), now)
    exitosa = True
    s.setblocking(0)

    pRecibidos = "NaN"

    print(filename)
    i = 0
    with conn:
        f = open("log/" + filename, "x")
        print('Connected by', addr)
        conn.send(b'OK')
        start_time = time.time()
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
            transfer_time = time.time()
            ready = select.select([conn], [], [], 10)
            while exitosa:
                elapsed_time = time.time() - start_time
                # print(elapsed_time)
                if ready[0]:
                    data = conn.recv(4096)
                    if data == b'Recibido correctamente':
                        print('Recibido correctamente')
                    elif data == b'Recibido incorrectamente':
                        print('Recibido incorrectamente')
                        exitosa = False
                    print("llega")
                    data = conn.recv(4096)
                    if data == b'Paquetes recibidos':
                        print("llega")
                        pRecibidos = str(int(conn.recv(4096), 2))
                if(elapsed_time > 10):
                    print("Tiempo de espera agotado")
                    exitosa = False
            print("Termina conexión")
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f.write("Fecha y hora de inicio: " + dt_string + "\n")
            f.write("Archivo enviado: " + fileToSend + "\n")
            f.write("Cliente: " + str(addr) + "\n")
            string_estado = "Verdadero" if exitosa else "Falso"
            f.write("Exitosa: " + string_estado + "\n")
            tiempo_tot = start_time - transfer_time
            f.write("Tiempo [s]: " + str(tiempo_tot) + "\n")
            f.write("Cantidad de paquetes enviados: " + str(i) + "\n")
            f.write("Cantidad de paquetes recibidos: " + pRecibidos + "\n")
            f.write("Cantidad de paquetes transmitidos: X" + "\n")
            f.write("Bytes enviados: " + "\n")
            f.write("Bytes recibidos: X" + "\n")
            f.write("Bytes transmitidos: X" + "\n")
            f.close()
            print("Registro en el log en el archivo " + filename)
            conn.close()

    s.close()
    # if not data: break
    # conn.sendall(data)
