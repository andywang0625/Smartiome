from Smartiome.Core.APIManager import *
import threading


@APIManager.plugin_register("CommandLine")
class CommandLine(threading.Thread):
    def __init__(self, eventManager=None):
        threading.Thread.__init__(self)
        self.eventManager = eventManager # Allows Plugins send event
        print("CommandLine is starting...")
        pass

    def run(self):
        while True:
            self.SendMessage()

    def SendMessage(self, PLUGINS=""):
        event = Event(type_=EType.DEFAULT)
        event.data["targets"] = input("Targets:")
        event.data["content"] = input("Content:")
        return event

    def ReceiveMessage(self, PLUGINS, args, str_list = True):
        if str_list:
            print(list(eval(args)))
        else:
            print(args)
        pass
