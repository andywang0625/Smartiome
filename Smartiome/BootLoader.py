from Smartiome.Core.EventManager import *
import sys
from datetime import datetime
from threading import *
import json
from Smartiome.Auxillaries.SystemLogger import *
from Smartiome.Auxillaries.Server import *
from Smartiome.Adaptors import *
from Smartiome.Core.APIManager import *
import threading

global lock
lock = threading.Lock()
lock.acquire()

# InitLogger for EventManager and BootLoader
logger = SystemLogger()

# Init EventManager
eventManager = EventManager(logger)

# Init APIManager
APIM = APIManager(eventManager)

# Resgiger Linstener for APIManager
eventManager.AddEventListener(EType.DEFAULT, APIM.ReadMessage)
# EventManager start
eventManager.Start()

# Your Code goes here
# APIM.cmdRevoke("SendMessage", "CommandLine")
APIM.ReadPluginsMessage()
lock.release()


'''
#OLD
from Smartiome.Adaptors.Controller.DeviceManager import *


def test():
    EVENT_INCOMING = EType.BROADCAST

    from Smartiome.Adaptors.Backend.TestEventSource import TestEventSource
    from Smartiome.Adaptors.Frontend.TestLinstener import TestLinstener

    listener1 = TestLinstener("Andy")
    listener2 = TestLinstener("Kanade")

    eventManager = EventManager()

    eventManager.AddEventListener(EVENT_INCOMING, listener1.ReadMessage)
    eventManager.AddEventListener(EVENT_INCOMING, listener2.ReadMessage)
    eventManager.Start()

    Source = TestEventSource(eventManager, EVENT_INCOMING)
    timer = Timer(2, Source.SendMessage)
    timer.start()



def TelegramBot():
    try:
        from Smartiome.Adaptors.Frontend.TelegramBotLinstener import TelegramBotInit, TelegramBotLinstener

        with open('Smartiome/Config/MyApi.json', 'r') as json_file:
            data = json.load(json_file)
        dp, updater = TelegramBotInit(data['api'], logger)
        tgb = TelegramBotLinstener(logger, dp, updater)
    except BaseException as e:
        logger.printError(info="TelegramBotLinstener Start")
    return tgb, dp, updater

def ConsoleSource():
    from Smartiome.Adaptors.Backend.ConsoleEventSource import ConsoleEventSource
    Source = ConsoleEventSource(eventManager, EType.COMMAND)
    Source.SendMessage()

def TelegramBotSource(logger, dp, updater):
    from Smartiome.Adaptors.Backend.TelegramBotSource import TelegramBotSource
    Source = TelegramBotSource(eventManager, EType.COMMAND, logger, dp, updater)

def ManagerServiceInit(port=2333):
    return ManagerService(logger=logger,eventManager=eventManager, port=port)

from Smartiome.Adaptors.Frontend.TTSLinstenner import TTSLinstener
tts = TTSLinstener()
tts.init(logger=logger, eventManager=EventManager, TYPE=EType.BROADCAST)
tgb, dp, updater = TelegramBot()
ms = ManagerServiceInit(14000)

ms.start()
TelegramBotSource(logger, dp, updater)
ConsoleSource()
'''
