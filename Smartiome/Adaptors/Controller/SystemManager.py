from Smartiome.Core.APIManager import *
import threading
import time
import sys
import platform
import psutil

"""
You may need to change all PluginSample to your own plugin's name
"""


@APIManager.plugin_register("SystemManager")
class SystemManager:
    SYSTEMVERSION = "April(Beta) 1.3.1"

    def __init__(self, __queue, logger, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue  # Allows APIManager Receive Messages
        self.logger = logger
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

        event = Event(type_ = EType.DEFAULT)
        event.data["target"] = args[0]
        event.data["source"] = args[1]
        event.data["recipient"] = args[2]
        event.data['content'] = args[3]
        self.__queue.put(event)  # Put the event to the __queue

    def ReceiveMessage(self, PLUGINS, event=None, str_list=False):
        """
        ReceiveMessage is the method that's called after API Manager got a message.
        arg1: PLUGINS uses to reflush the list of APIs
        arg2: Args is the message passes into
        arg3: str_list=True. If this method is called by eval, you may leave it True; otherwise, you need to pass False
        """
        if str_list:
            event = list(eval(event))
        # print(event.data["content"])
        # Handling the messages
        if "sysver" in event.data["content"]:
            info = self.getSystemVersion()
        elif "lsver" in event.data["content"]:
            info = self.getLastSupportedVersion()
        elif "pyver" in event.data["content"]:
            info = self.getPythonVersionInfo()
        elif "plat" in event.data["content"]:
            info = self.getPlatform()
        elif "sysinfo" in event.data["content"]:
            info = self.getSystemInfo()
        else:
            info = "Command not found"
        self.logger.printInfo(event.data["content"]+" Called")
        self.SendMessage(event.data["source"],
                         event.data["target"],
                         event.data["recipient"],
                         info)
        pass

    def getSystemVersion(self):
        return self.SYSTEMVERSION

    def getLastSupportedVersion(self):
        return self.SYSTEMVERSION

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

    def start_worker(self):
        """
        start_worker uses to start the worker
        No need to change anything, unless you need to do so.
        """
        t = threading.Thread(target=self.worker, args=(self,))
        t.setDaemon(True)

        # You may not need to start it as a Controller
        # t.start()

    def worker(self):
        """
        Things need to keep running
        """
        print("SystemManager Started")
        time.sleep(1)  # Prevent errors from being displayed during initialization
        while True:
            time.sleep(0.3)  # Prevent errors from being displayed during running
            self.SendMessage(self) # Calling SendMessage
