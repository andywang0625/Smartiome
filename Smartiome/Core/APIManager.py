from Smartiome.Core.EventManager import *


class APIManager(object):
    PLUGINS = {}
    def __init__(self, logger, EventManager):
        self.logger = logger
        self.EventManager = EventManager

    def ReadMessage(self, event):
        #print(event)
        """
        ReadMessage Method is for being a Linstener
        arg1: Event(event) No BB
        """
        if event.type_ == EType.BROADCAST:
            # Enabled Broadcast Interfaces
            self.PLUGINS["CommandLine"]()\
                .ReceiveMessage(self.PLUGINS, event.data, need_eval=False)
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
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
