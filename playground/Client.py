from socket import *
import threading
import pickle

class client(threading.Thread):
    def __init__(self, clientID, server, port=2333):
        threading.Thread.__init__(self)
        self.Server = server
        self.Port = port
        self.Address = (self.Server,self.Port)
        self.Socket = socket(AF_INET, SOCK_DGRAM)
        self.Socket.settimeout(2)
    def clientThread(self):
        while True:
            message = []
            message.append(input("Client> Type:"))
            message.append(input("Client> Message:"))
            message = pickle.dumps(message)
            self.Socket.sendto(message, self.Address)
            try:
                returnMessage, serverAddress = self.Socket.recvfrom(2048)
            except:
                print("Client> None!")
                continue
            print("Client> from "+self.Address[0]+":"+str(self.Address[1])+"- Message Returned:"+returnMessage.decode('utf-8'))
    def run(self):
        self.clientThread()


cli = client(1, "localhost", port=16000)
cli.start()
