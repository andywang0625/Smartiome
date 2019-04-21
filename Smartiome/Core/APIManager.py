from Smartiome.Core.EventManager import *
from queue import Queue, Empty
from Smartiome.Auxillaries.SystemLogger import *

"""
Generic Message Format:
    data["target"]: str(plugin_name)
    data["source"]: str(plugin_name)
    (opt)data["recipient"]: str(recipient_id)
    data["content"]: list(content or command)
"""

class APIManager(object):
    PLUGINS = {}
    PLUGINS_EVENTS_QUEUE = Queue()
    logger = SystemLogger()

    def __init__(self, EventManager):
        self.EventManager = EventManager

    def ReadPluginsMessage(self):
        print("Started")
        while True:
            try:
                event = self.PLUGINS_EVENTS_QUEUE.get(block=False)
                # print(event)
                self.SendMessage(event)
            except Empty:
                pass

    def ReadMessage(self, event):
        #print(event)
        """
        ReadMessage Method is for being a Linstener
        arg1: A event - type: Event()
        """
        #self.PLUGINS["CommandLine"].ReceiveMessage(self.PLUGINS, event.data, str_list=False)
        if event.type_ == EType.DEFAULT:
            # Enable DEFAULT Interfaces
            if event.data["targets"] == "revoke":
                self.cmdRevoke(event.data["cmd"],
                               event.data["plugin"],
                                event.data["args"])
            #print(event)
            if event.data["targets"] in self.PLUGINS:
                # print("yes")
                # self.PLUGINS["CommandLine"]().ReceiveMessage()
                self.PLUGINS[event.data["targets"]].ReceiveMessage(
                    self.PLUGINS,
                    event=event)
            else:
                self.logger.printError("Calling "+event.data["targets"], target="APIManager")
            #    else:
            #        print("Not in the list of plugins")

            #for func in self.PLUGINS:
            #    func().ReceiveMessage(self.PLUGINS,event., event.data, str_list=False)
            #self.PLUGINS["CommandLine"]()\
            #    .ReceiveMessage(self.PLUGINS, event.data, str_list=False)
        #pass message back to plugins
        pass

    def SendMessage(self, event):
        """
        SendMessage Method is for being an Event Source
        arg1: Event(event)
        """
        #print(event)
        self.EventManager.SendEvent(event)


    def cmdRevoke(self, cmd, plugin="", args=[]):
        """
        cmdRevoke calls a method in the specified plugin object
        arg1: string(cmd) the cmd is going to revoke
        arg2: string(plugin) the the plugin object of the method
        arg3: args (need to implement)
        """
        if plugin is ():
            print("No specified plugin")
            return
        else:
            if args != []:
                self.SendMessage(eval("self.PLUGINS[\""+plugin+"\"]()."+cmd+"(self.PLUGINS, "
                     + str(args)+")")) # Send args as str
                # self.PLUGINS[plugin]().cmd(args) # Fucked up
            else:
                self.SendMessage(eval("self.PLUGINS[\""+plugin+"\"]()."+cmd+"(self.PLUGINS"
                     +")")) # Send args as str

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            obj = object.__new__(plugin)
            cls.PLUGINS.update({plugin_name:obj})
            obj.__init__(cls.PLUGINS_EVENTS_QUEUE, cls.logger)
            print(plugin_name+" has been activitied.")
            return obj
        return wrapper
