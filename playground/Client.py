from socket import *
import threading
import pickle
import time
import sys
import platform
import psutil

class client(threading.Thread):
    CLIENTVERSION = "April(Beta)-Client 1.4.1"
    def __init__(self, clientID, server, port=2333):
        threading.Thread.__init__(self)
        self.Server = server
        self.Port = port
        self.Address = (self.Server,self.Port)
        self.Socket = socket(AF_INET, SOCK_DGRAM)
        self.Socket.settimeout(2)
    def clientThread(self):
        while True:
            message = {}
            # message["device"] = (input("Client> Type:"))
            # message["content"] = (input("Client> Message:"))
            # message = pickle.dumps(message)
            # self.Socket.sendto(message, self.Address)
            try:
                returnMessage, serverAddress = self.Socket.recvfrom(2048)
                returnMessage = pickle.loads(returnMessage)
                if returnMessage["content"] == "ping":
                    message["type"] = "basic"
                    message["content"] = "PINGDONE"
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "cliver":
                    message["type"] = "info"
                    message["content"] = self.getClientVersion()
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "lsver":
                    message["type"] = "info"
                    message["content"] = self.getLastSupportedVersion()
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "pyver":
                    message["type"] = "info"
                    message["content"] = self.getPythonVersionInfo()
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "pla":
                    message["type"] = "info"
                    message["content"] = self.getPlatform()
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "sysinfo":
                    message["type"] = "info"
                    message["content"] = self.getSystemInfo()
                    message = pickle.dumps(message)
                    self.Socket.sendto(message, self.Address)
                elif returnMessage["content"] == "!EOF":
                    print("DeviceManager Clear Revoked")
                    return
            except:
                # print("Client> None!")
                continue

    def run(self):
        message = {}
        message["device"] = (input("Client> Name:"))
        message["content"] = "register"
        message["type"] = "basic"
        message = pickle.dumps(message)
        self.Socket.sendto(message, self.Address)
        try:
            returnMessage, serverAddress = self.Socket.recvfrom(2048)
            if returnMessage.decode('utf-8') == "ADDED":
                print("Device Added")
            elif returnMessage == "NONEED".decode('utf-8'):
                print("No Need to register device")
            self.clientThread()
        except BaseException as e:
            print("Not able to reach the server"+str(e))

    def getClientVersion(self):
        return self.CLIENTVERSION

    def getLastSupportedVersion(self):
        return self.CLIENTVERSION

    def getPythonVersionInfo(self):
        a = sys.version.split(" ", maxsplit=1)
        b = a[1].split(")", maxsplit=1)
        c = b[1].split("[")
        verstr = a[0]
        detailver = b[0].lstrip("(")
        compiler = c[1].rstrip("]")
        return verstr, detailver, compiler

    def getSystemInfo(self):
        info = "RAM Usage:\t"+str(psutil.virtual_memory().percent)+"%"+"\n"
        psutil.cpu_percent(None)
        time.sleep(3)
        info += "CPU Usage:\t"+str(psutil.cpu_percent(None))+"%\n"
        info += "Disk(s) Usage:\t"+str(psutil.disk_io_counters(perdisk=True))
        return info

    def getPlatform(self):
        return platform.platform()


cli = client(1, "localhost", port=14000)
cli.start()
cli.join()
