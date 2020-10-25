# Echo client program
import socket
import hashlib
import time
import timeit

HOST = 'localhost'  # '192.168.2.133'    # The remote host
PORT = 7735  # The same port as used by the server
folder = './save_content/'
p = 0.05
file_sended = 'video1.mkv'


def bytes_of(s):
    return len(s.encode('utf-8'))


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((HOST, PORT))
        self.sock.setblocking(0)
        self.p = p
        self.expected_seq = 0
        self.ack_seq = 0
        self.timeout = 0.1
        self.packet_loss = False

    # Carry bit used in one's combliment
    def carry_around_add(self, num_1, num_2):
        c = num_1 + num_2
        return (c & 0xffff) + (c >> 16)

    # Calculate the checksum of the data only. Return True or False
    def checksum(self, msg):
        """Compute and return a checksum of the given data"""
        msg = msg.decode('utf-8')
        if len(msg) % 2:
            msg += "0"
        s = 0
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
            s = self.carry_around_add(s, w)
        return ~s & 0xffff

    def receive(self):
        print("Empieza")
        global data
        file = open('./save_content/'+file_sended, 'wb')
        try:
            while True:
                try:
                    data, address = self.sock.recvfrom(4096)
                    data = pickle.loads(data)
                    prob = random.random()
                    if self.expected_seq != int(data.sequenceNumber, 2):
                        continue
                    elif data.checksum != self.checksum(data.packet):
                        continue

                    elif prob <= self.p:
                        print('Packet Loss, Sequence Number = ',
                              int(data.sequenceNumber, 2))
                        continue

                except socket.error:
                    continue
                except KeyboardInterrupt:
                    self.sock.close()
                    sys.exit(0)

                file.write(data.packet)
                sendACK = Acknowledgment(data.sequenceNumber)
                self.sock.sendto(pickle.dumps(sendACK), address)
                if data.eof == 1:
                    print('File Received.')
                    sys.exit(0)
                self.expected_seq += 1
            file.close()
        except:
            pass


def main():
    # Arguments are passed in order of acceptance in the command line arguments
    client = Client()
    # try:
    client.receive()
    #print("Run Time:", timeit.timeit(client.receive(), number=1))
    # except:
    #   print("Error occured while sending")


if __name__ == "__main__":
    main()
