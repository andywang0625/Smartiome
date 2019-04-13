from Smartiome.Auxillaries.EventManager import *
from Smartiome.Auxillaries.SystemManager import *


class SystemManager:
    def __init__(self, logger, eventManager):
        self.logger = logger
        self.__eventManager = eventManager
        #Do Nothing
        pass

    def info(self, update):
        try:
            event = Event(type_ = EType.OUTPUT)
            verstr, detailver, compiler = getPythonVersionInfo()
            message = getSystemVersion()+"\n"+getPlatform()+"\n"+verstr+"  "+detailver+"  "+compiler
            event.data["Event"] = message
            event.data["ChatId"] = update.message.chat_id
        except BaseException as e:
            self.logger.printError("Getting Info", target="SystemManager")
            event = Event(type_ = EType.BROADCAST)
            event.data["Event"] = "Failed to get system infomation"
            event.data["ChatId"] = update.message.chat_id
        self.__eventManager.SendEvent(event)
