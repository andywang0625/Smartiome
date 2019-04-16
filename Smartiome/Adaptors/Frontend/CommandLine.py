from Smartiome.Core.APIManager import *


@APIManager.plugin_register("CommandLine")
class CommandLine:
    def __init__(self, eventManager=''):
        self.eventManager = eventManager # Allows Plugins send event
        pass

    def SendMessage(self, PLUGINS):
        event = Event(type_=EType.BROADCAST)
        event.data["content"] = input("Content:")
        return event

    def ReceiveMessage(self, PLUGINS, args, need_eval = True):
        if need_eval:
            print(list(eval(args)))
        else:
            print(args)
        pass
