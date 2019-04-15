from socket import *
import threading

class server(threading.Thread):
    def __init__(self, serverID, port=2333):
        threading.Thread.__init__(self)
        self.Port = port
        self.Socket = socket(AF_INET, SOCK_DGRAM)

    def serverThread(self):
        self.Socket.bind(('', self.Port))
        print("waitint")
        while True:
            message, clientAddress = self.Socket.recvfrom(2048)
            print(message.decode('utf-8')+" from "+str(clientAddress))
            self.Socket.sendto("gotta!".encode('utf-8'), clientAddress)

    def run(self):
        self.serverThread()

ser = server(1, 14000)
ser.start()
