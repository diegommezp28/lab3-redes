#!/usr/bin/env python

import socket
import sys

HOST = '127.0.0.1'
PORT = 50007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)
fname = 'fromserver.png'

try:

       sock.sendall(b"GET\r\n")
       data = sock.recv(4096)

       if data:
           txt = data.strip()
           print ('--%s--' % txt)

           if txt == 'OK':

               sock.sendall("GET_SIZE\r\n")
               data = sock.recv(4096)

               if data:
                   txt = data.strip()
                   print ('--%s--' % txt)

                   if txt.startswith('SIZE'):

                       tmp = txt.split()
                       size = int(tmp[1])

                       print ('--%s--' % size)

                       sock.sendall("GET_IMG\r\n")

                       myfile = open(fname, 'wb')

                       amount_received = 0
                       while amount_received < size:
                           data = sock.recv(4096)
                           if not data :
                               break
                           amount_received += len(data)
                           print (amount_received)

                           txt = data.strip('\r\n')

                           if 'EOF' in str(txt) :
                               print ('Image received successfully')
                               myfile.write(data)
                               myfile.close()
                           else :
                               myfile.write(data)
finally:
       sock.close()