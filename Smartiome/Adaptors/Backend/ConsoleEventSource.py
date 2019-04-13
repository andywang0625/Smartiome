import sys
from Smartiome.Auxillaries.EventManager import *


class ConsoleEventSource:
    def __init__(self, eventManager, type):
        self.__eventManager = eventManager
        self.__type=type

    def SendMessage(self):
        event = Event(type_=self.__type)
        while True:
            event.data["Event"] = input("Console:")
            self.__eventManager.SendEvent(event)
