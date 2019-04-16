import os
from Smartiome.Core.EventManager import *
from Smartiome.Auxillaries.SystemManager import *
from Smartiome.Adaptors.Controller.Controller import *


class ControllerHelper(Controller):
    def __init__(self, logger, eventManager, RegisteredControllers):
        self.logger = logger
        self.__eventManager = eventManager
        self.ControllersEnabled = RegisteredControllers
        self.Controllers = []
        self.ControllersDir = "./Smartiome/Adaptors/Controller"
        for filename in os.listdir(self.ControllersDir):
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

    def list(self, update, controller):
        try:
            #a = filter(lambda x: "__" not in x and callable(getattr(self,x)), dir(self.ControllersDir+"/"+str(controller)+".py"))
            #temlist = list(a)
            #message = str(temlist)
            message = str(dir(self.ControllersDir+"/"+str(controller)+".py"))
            #message = str(self.ControllersDir+"/"+str(controller)+".py")
            event = Event(type_=EType.OUTPUT)
            event.data["Event"] = message
            event.data["ChatId"] = update.message.chat_id
        except BaseException as e:
            self.logger.printError("Getting Methods-"+str(e), target="ControllerHelper")
            event = Event(type_ = EType.BROADCAST)
            event.data["Event"] = "Failed to get methods"
            event.data["ChatId"] = update.message.chat_id
        self.__eventManager.SendEvent(event)

    def help(self, update):
        try:
            event = Event(type_ = EType.OUTPUT)
            verstr, detailver, compiler = getPythonVersionInfo()
            message = """
.list - Show Installed Controller(s)
.enabled - Show Enabled Controller(s)
            """
            event.data["Event"] = message
            event.data["ChatId"] = update.message.chat_id
        except BaseException as e:
            self.logger.printError("Getting Help", target=str(self))
            event = Event(type_ = EType.BROADCAST)
            event.data["Event"] = "Failed to get help"
            event.data["ChatId"] = update.message.chat_id
        self.__eventManager.SendEvent(event)
