from Smartiome.Core.APIManager import *
import threading
import time
from socket import *
import pickle


"""
You may need to change all PluginSample to your own plugin's name
"""


@APIManager.plugin_register("DeviceManager")
class DeviceManager:
    devices = {}
    def __init__(self, __queue, logger, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue  # Allows APIManager Receive Messages
        self.logger = logger
        self.Socket = socket(AF_INET, SOCK_DGRAM)
        self.ping_success = False
        pass

    def SendMessage(self, *args, **kwargs):
        """
        SendMessage helps the plugin send Events back to the APIManager
        arg1: *args
        arg2: **kwargs
        """

        """
        Generic Message Format:
            data["target"]: str(plugin_name)
            data["source"]: str(plugin_name)
            (opt)data["recipient"]: str(recipient_id)
            data["content"]: list(content or command)
        """

        self.__queue.put(args[0])  # Put the event to the __queue

    def ReceiveMessage(self, PLUGINS, event=None, str_list=False):
        """
        ReceiveMessage is the method that's called after API Manager got a message.
        arg1: PLUGINS uses to reflush the list of APIs
        arg2: Args is the message passes into
        arg3: str_list=True. If this method is called by eval, you may leave it True; otherwise, you need to pass False
        """
        if str_list:
            event = object(eval(event))
        if "list" in event.data["content"]:
            NewEvent = Event(type_ = EType.DEFAULT)
            NewEvent.data["target"] = event.data["source"]
            NewEvent.data["source"] = "DeviceManager"
            NewEvent.data["recipient"] = event.data["recipient"]
            NewEvent.data["content"] = str(self.devices)
            self.SendMessage(NewEvent)

        elif "clear" in event.data["content"]:
            NewEvent = Event(type_ = EType.DEFAULT)
            NewEvent.data["target"] = event.data["source"]
            NewEvent.data["source"] = "DeviceManager"
            NewEvent.data["recipient"] = event.data["recipient"]
            NewEvent.data["content"] = str(self.devices)
            message = {}
            message["content"] = "!EOF"
            message = pickle.dumps(message)
            for dev in self.devices.values():
                self.Socket.sendto(message, dev)
            self.devices = {}
            self.SendMessage(NewEvent)

        elif "ping" in event.data["content"]:
            message = {}
            message["content"] = "ping"
            message = pickle.dumps(message)
            if event.data["content"].split(" ")[1] in self.devices.keys():
                self.Socket.sendto(message,
                                   self.devices[event.data["content"]
                                                .split(" ")[1]])
                time.sleep(3)
                if self.ping_success:
                    self.ping_success = False
                    NewEvent = Event(type_ = EType.DEFAULT)
                    NewEvent.data["target"] = event.data["source"]
                    NewEvent.data["source"] = "DeviceManager"
                    NewEvent.data["recipient"] = event.data["recipient"]
                    NewEvent.data["content"] = "Success: "+event.data["content"].split(" ")[1]
                    self.SendMessage(NewEvent)
                else:
                    self.ping_success = False
                    NewEvent = Event(type_ = EType.DEFAULT)
                    NewEvent.data["target"] = event.data["source"]
                    NewEvent.data["source"] = "DeviceManager"
                    NewEvent.data["recipient"] = event.data["recipient"]
                    NewEvent.data["content"] = "Failed: "+event.data["content"].split(" ")[1]
                    self.SendMessage(NewEvent)
            else:
                NewEvent = Event(type_ = EType.DEFAULT)
                NewEvent.data["target"] = event.data["source"]
                NewEvent.data["source"] = "DeviceManager"
                NewEvent.data["recipient"] = event.data["recipient"]
                NewEvent.data["content"] = "Device has not registered yet"
                self.SendMessage(NewEvent)
        else:
            if event.data["content"].split(" ")[1] != ""\
             and event.data["content"].split(" ")[1] in self.devices.keys():
                if "cliver" in event.data["content"]:
                    message = {}
                    message["content"] = "cliver"
                    message = pickle.dumps(message)
                    if event.data["content"].split(" ")[1] in self.devices.keys():
                        self.Socket.sendto(message,
                                           self.devices[event.data["content"]
                                                        .split(" ")[1]])
                elif "lsver" in event.data["content"]:
                    message = {}
                    message["content"] = "lsver"
                    message = pickle.dumps(message)
                    if event.data["content"].split(" ")[1] in self.devices.keys():
                        self.Socket.sendto(message,
                                           self.devices[event.data["content"]
                                                        .split(" ")[1]])
                elif "pyver" in event.data["content"]:
                    message = {}
                    message["content"] = "pyver"
                    message = pickle.dumps(message)
                    if event.data["content"].split(" ")[1] in self.devices.keys():
                        self.Socket.sendto(message,
                                           self.devices[event.data["content"]
                                                        .split(" ")[1]])
                elif "pla" in event.data["content"]:
                    message = {}
                    message["content"] = "pla"
                    message = pickle.dumps(message)
                    if event.data["content"].split(" ")[1] in self.devices.keys():
                        self.Socket.sendto(message,
                                           self.devices[event.data["content"]
                                                        .split(" ")[1]])
                elif "sysinfo" in event.data["content"]:
                    message = {}
                    message["content"] = "sysinfo"
                    message = pickle.dumps(message)
                    if event.data["content"].split(" ")[1] in self.devices.keys():
                        self.Socket.sendto(message,
                                           self.devices[event.data["content"]
                                                        .split(" ")[1]])
                else:
                    NewEvent = Event(type_ = EType.DEFAULT)
                    NewEvent.data["target"] = event.data["source"]
                    NewEvent.data["source"] = "DeviceManager"
                    NewEvent.data["recipient"] = event.data["recipient"]
                    NewEvent.data["content"] = "Command not found"
                    self.SendMessage(NewEvent)
                    return
                time.sleep(5)
                if self.tmp_info != "":
                    NewEvent = Event(type_ = EType.DEFAULT)
                    NewEvent.data["target"] = event.data["source"]
                    NewEvent.data["source"] = "DeviceManager"
                    NewEvent.data["recipient"] = event.data["recipient"]
                    NewEvent.data["content"] = self.tmp_info
                    self.tmp_info = ""
                    self.SendMessage(NewEvent)
                else:
                    NewEvent = Event(type_ = EType.DEFAULT)
                    NewEvent.data["target"] = event.data["source"]
                    NewEvent.data["source"] = "DeviceManager"
                    NewEvent.data["recipient"] = event.data["recipient"]
                    NewEvent.data["content"] = "Connection Failed"
                    self.tmp_info = ""
                    self.SendMessage(NewEvent)
            else:
                NewEvent = Event(type_ = EType.DEFAULT)
                NewEvent.data["target"] = event.data["source"]
                NewEvent.data["source"] = "DeviceManager"
                NewEvent.data["recipient"] = event.data["recipient"]
                NewEvent.data["content"] = "Please enter a valid hostname"
                self.tmp_info = ""
                self.SendMessage(NewEvent)
        # Handling the messages
        pass

    def start_worker(self):
        """
        start_worker uses to start the worker
        No need to change anything, unless you need to do so.
        """
        t = threading.Thread(target=self.worker, args=())
        t.setDaemon(True)

        # You may not need to start it as a Controller
        t.start()

    def worker(self):
        """
        Things need to keep running
        """
        print("DeviceManager Started")
        self.Socket.bind(('', 14000))
        while True:
            message, clientAddress = self.Socket.recvfrom(65535)
            message = pickle.loads(message)
            # print(str(message)+" from "+str(clientAddress))
            if message["type"] == "basic":
                if message["content"] == "PINGDONE":
                    self.ping_success = True
                if message["content"] == "register":
                    if clientAddress not in self.devices.values():
                        try:
                            self.devices[message["device"]] = clientAddress
                            self.Socket.sendto("ADDED".encode('utf-8'), clientAddress)
                        except:
                            self.Socket.sendto("NONEED".encode('utf-8'), clientAddress)
                    else:
                        self.Socket.sendto("NONEED".encode('utf-8'), clientAddress)
            elif message["type"] == "info":
                self.tmp_info = message["content"]
            # self.SendMessage() # Calling SendMessage
