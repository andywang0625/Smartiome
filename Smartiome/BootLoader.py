from Smartiome.Auxillaries.EventManager import *
import sys
from datetime import datetime
from threading import *
import json
from Smartiome.Auxillaries.SystemLogger import *

logger = SystemLogger()

def test():
    EVENT_INCOMING = "Event_Incoming"

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

eventManager = EventManager()
EVENT_INCOMING = "Incoming"
EVENT_COMMAND = "Command"

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
    Source = ConsoleEventSource(eventManager, EVENT_COMMAND)
    Source.SendMessage()

def TelegramBotSource(logger, dp, updater):
    from Smartiome.Adaptors.Backend.TelegramBotSource import TelegramBotSource
    Source = TelegramBotSource(eventManager, EVENT_COMMAND, logger, dp, updater)

from Smartiome.Adaptors.Frontend.TTSLinstenner import TTSLinstener
tts = TTSLinstener()
tts.init(logger=logger, eventManager=EventManager, TYPE=EVENT_INCOMING)

tgb, dp, updater = TelegramBot()
eventManager.AddEventListener(EVENT_INCOMING, tts.ReadMessage)
eventManager.AddEventListener(EVENT_COMMAND, tts.ReadMessage)
eventManager.AddEventListener(EVENT_INCOMING, tgb.talkToMaster)
eventManager.AddEventListener(EVENT_COMMAND, tgb.talkToMaster)



eventManager.Start()
TelegramBotSource(logger, dp, updater)




#ConsoleSource()
