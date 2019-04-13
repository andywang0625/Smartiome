import os
from Smartiome.Auxillaries.EventManager import *
from Smartiome.Auxillaries.SystemManager import *


class ControllerHelper:
    def __init__(self, logger, eventManager, RegisteredControllers):
        self.logger = logger
        self.__eventManager = eventManager
        self.ControllersEnabled = RegisteredControllers
        self.Controllers = []
        for filename in os.listdir('./Smartiome/Adaptors/Controller'):
            if ".py" in filename:
                self.Controllers.append(filename)

    def list(self, update):
        try:
            event = Event(type_ =EType.OUTPUT)
            message = str(self.Controllers)
            event.data["Event"] = message
            event.data["ChatId"] = update.message.chat_id
        except BaseException as e:
            self.logger.printError("Getting Info", target="ControllerHelper")
            event = Event(type_ = EType.BROADCAST)
            event.data["Event"] = "Failed to get controllers"
            event.data["ChatId"] = update.message.chat_id
        self.__eventManager.SendEvent(event)

    def enabled(self, update):
        try:
            message = ""
            event = Event(type_=EType.OUTPUT)
            for conenabled in self.ControllersEnabled:
                message += str(conenabled)+"\n"
            event.data["Event"] = message
            event.data["ChatId"] = update.message.chat_id
        except BaseException as e:
            self.logger.printError("Getting Info", target="ControllerHelper")
            event = Event(type_ = EType.BROADCAST)
            event.data["Event"] = "Failed to get enabled controllers"
            event.data["ChatId"] = update.message.chat_id
        self.__eventManager.SendEvent(event)
