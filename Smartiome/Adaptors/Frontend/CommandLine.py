from Smartiome.Core.APIManager import *
import threading
import time


@APIManager.plugin_register("CommandLine")
class CommandLine:
    def __init__(self, __queue, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue
        print("CommandLine is starting...")
        self.start_worker()
        pass

    def SendMessage(self, PLUGINS=""):
        event = Event(type_ = EType.DEFAULT)
        event.data["targets"] = input("Targets:")
        event.data["content"] = input("Content:")
        self.__queue.put(event)
        # print(self.__queue.qsize())

    def ReceiveMessage(self, PLUGINS, args, str_list=True):
        # print("called")
        if str_list:
            print(list(eval(args)))
        else:
            print(args)
        pass

    def start_worker(self):
        t = threading.Thread(target=self.worker, args=())
        t.setDaemon(True)
        t.start()

    def worker(self):
        print("CommandLine Started")
        time.sleep(1)
        while True:
            time.sleep(0.3)
            self.SendMessage(self)
