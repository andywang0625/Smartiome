from Smartiome.Auxillaries.Server import *
from Smartiome.Auxillaries.EventManager import *
import pickle


class ManagerService(threading.Thread):
    def __init__(self, logger, eventManager, port=2333):
        threading.Thread.__init__(self)
        self.Port = port
        self.logger = logger
        self.Socket = socket(AF_INET, SOCK_DGRAM)
        self.__eventManager = eventManager
        self.logger = logger
        self.__eventManager = eventManager
        self.deviceList = []
        pass

    def serverThread(self):
        self.Socket.bind(('localhost', self.Port))
        self.logger.printInfo("Server Started", target="serverThread")
        while True:
            try:
                message, clientAddress = self.Socket.recvfrom(2048)
                message = pickle.loads(message)
                if message[0] == "BROADCAST":
                    event = Event(type_=EType.BROADCAST)
                else:
                    event = Event(type_=EType.DEVICEEVENT)
                event.data["Event"] = message
                event.data["Addr"] = str(clientAddress)
                self.__eventManager.SendEvent(event)
            except BaseException as e:
                self.logger.printError(str(e), target="serverThread")
            self.Socket.sendto(CType.SUCCESS.encode('utf-8'), clientAddress)

    def run(self):
        self.serverThread()

    def ReadMessage(self, event):
        try:
            event.data["Event"][0] #If Event Header exsit

            if event.data["Event"][0] == "INIT":
                self.deviceList.append(event.data["Addr"])

        except:
            self.logger.printError("ReadMessage", target="ManagerService")

    def list(self):
        print(str(self.deviceList))

    def ping(self, ip, port) -> bool:
        addr = (ip, port)
        message = []
        message.append("PING")
        message = pickle.dumps(message)
        self.server.Socket.sendto(CType.SUCCESS.encode('utf-8'), addr)

        pass
