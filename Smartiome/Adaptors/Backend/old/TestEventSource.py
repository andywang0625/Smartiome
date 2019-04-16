import sys
from Smartiome.Core.EventManager import *


class TestEventSource:
    def __init__(self, eventManager, type):
        self.__eventManager = eventManager
        self.__type=type

    def SendMessage(self):
        event = Event(type_=self.__type)
        event.data["Event"] = "EventMessage"

        self.__eventManager.SendEvent(event)
