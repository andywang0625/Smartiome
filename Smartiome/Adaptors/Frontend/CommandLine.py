from Smartiome.Core.APIManager import *
from prettytable import PrettyTable
import threading
import time


@APIManager.plugin_register("CommandLine")
class CommandLine:
    def __init__(self, __queue, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue
        print("CommandLine is starting...")
        pass

    def SendMessage(self, PLUGINS=""):
        event = Event(type_ = EType.DEFAULT)
        event.data["target"] = input("Target:")
        event.data["source"] = "CommandLine"
        event.data["recipient"] = input("Recipient Id:")
        event.data["content"] = input("Content:")
        self.__queue.put(event)
        # print(self.__queue.qsize())

    def ReceiveMessage(self, PLUGINS, event=None, str_list=False):
        if event:
            # print("called")
            if str_list:
                event = Event(eval(event))
            x = PrettyTable(["Event Attributes", "Values"])
            x.align["Event Attributes"] = "1"
            x.padding_width = 1
            x.add_row(["Target:", event.data["target"]])
            x.add_row(["Source:", event.data["source"]])
            x.add_row(["Recipient Id:", event.data["recipient"]])
            x.add_row(["Message Content:", event.data["content"]])
            print("\n")
            print(x)
        pass

    def start_worker(self):
        t = threading.Thread(target=self.worker, args=())
        t.setDaemon(True)
        t.start()

    def worker(self):
        print("CommandLine Started")
        time.sleep(1)
        # lock.release()
        while True:
            time.sleep(0.3)
            self.SendMessage()
