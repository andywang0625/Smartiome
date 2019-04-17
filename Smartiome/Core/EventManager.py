from queue import Queue, Empty
from threading import *

class EType(object):
    DEFAULT = 0

class EventManager:
    def __init__(self, logger):
        self.__eventQueue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__Run)
        self.__handlers = {}
        self.logger = logger

    def __Run(self):
        while self.__active == True:
            try:
                event = self.__eventQueue.get(block=False)
                self.__EventProcess(event)
            except Empty:
                pass

    def __EventProcess(self, event):
        if event.type_ in self.__handlers:
            for handler in self.__handlers[event.type_]:
                handler(event)

    def Start(self):
        self.__active = True
        self.__thread.start()

    def Stop(self):
        self.__active=False
        self.__thread.join()

    def AddEventListener(self, type_, handler):
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []

        self.__handlers[type_] = handlerList

        if handler not in handlerList:
            handlerList.append(handler)
        # self.__handlers = handlerList

    def RemoveEventLinstener(self, type_, handler):
        try:
            handlerList = self.__handlers[type_]
            if handler in handlerList:
                handlerList.pop(handler)
            self.__handlers = handlerList
            pass
        except:
            self.logger.printError("RemoveEventLinstener",
                                   target="EventManager")


    def SendEvent(self, event):
        self.__eventQueue.put(event)


class Event:
    def __init__(self, type_=None):
        self.type_ = type_
        self.data = {}
