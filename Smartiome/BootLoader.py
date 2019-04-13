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

def TelegramBot():
    try:
        from Smartiome.Adaptors.Frontend.TelegramBotLinstener import TelegramBotInit, TelegramBotLinstener

        with open('Smartiome/Config/MyApi.json', 'r') as json_file:
            data = json.load(json_file)
        dp, updater = TelegramBotInit(data['api'], logger)
        tgb = TelegramBotLinstener(logger, dp, updater)
        eventManager.AddEventListener(EVENT_INCOMING, tgb.talkToMaster)
        #em = EventManager()
        #em.AddEventListener()
        #TelegramBotLinstener(logger,data['api'])
    except BaseException as e:
        logger.printError(info="TelegramBotLinstener Start")

def TTS():
    try:
        from Smartiome.Adaptors.Frontend.TTSLinstenner import TTSLinstener
        tts = TTSLinstener(logger)
        eventManager.AddEventListener(EVENT_INCOMING, tts.ReadMessage)
    except BaseException as e:
        logger.printError(action="TTS Start", info=e)

def ConsoleSource():
    from Smartiome.Adaptors.Backend.ConsoleEventSource import ConsoleEventSource
    Source = ConsoleEventSource(eventManager, EVENT_INCOMING)
    Source.SendMessage()


TelegramBot()
TTS()

eventManager.Start()

ConsoleSource()
