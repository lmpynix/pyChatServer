import socket, threading

HOST = ''
PORT = 51234 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()


class chatServer(threading.Thread):
    def __init__(self, tuplein):
        threading.Thread.__init__(self)
        self.socket = tuplein[0]
        self.address= tuplein[1]

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print ('%s:%s connected.' % self.address)
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            for c in clients:
                if c is not self:
                    c.socket.send(data)
        self.socket.close()
        print ('%s:%s disconnected.' % self.address)
        lock.acquire()
        clients.remove(self)
        lock.release()

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    chatServer(s.accept()).start()