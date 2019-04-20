import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from Smartiome.Core.EventManager import *
from Smartiome.Auxillaries.SystemConf import *
from Smartiome.Auxillaries.UserControl import *
from Smartiome.Core.APIManager import *
import threading
import time


@APIManager.plugin_register("TelegramBot")
class TelegramBot(threading.Thread):
    def __init__(self, __queue, eventManager=None):
        super().__init__(self)
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue
        print("CommandLine is starting...")
        self.start_worker(self)
        pass

    def SendMessage(self, PLUGINS=""):
        event = Event(type_ = EType.DEFAULT)
        event.data["targets"] = input("Targets:")
        event.data["content"] = input("Content:")
        self.__queue.put(event)
        # print(self.__queue.qsize())

    def ReceiveMessage(self, PLUGINS, args, str_list=True):
        # print("called")
        if str_list:
            print(list(eval(args)))
        else:
            print(args)
        pass

    def start_worker(self):
        t = threading.Thread(target=self.worker, args=(self,))
        t.setDaemon(True)
        t.start()

    def worker(self):
        print("CommandLine Started")
        time.sleep(1)
        while True:
            time.sleep(0.3)
            self.SendMessage(self)
