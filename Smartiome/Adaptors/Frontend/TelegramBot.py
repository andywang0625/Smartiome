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
import json

@APIManager.plugin_register("TelegramBot")
class TelegramBot:
    def __init__(self, __queue, logger, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue  # Allows APIManager Receive Messages
        self.logger = logger
        try:
            with open('Smartiome/Config/MyApi.json', 'r') as json_file:
                data = json.load(json_file)
            self.logger.printInfo("Loading config of TelegramBot",
                                  target="TelegramBot")
            self.updater = Updater(data["api"])
            self.dp = self.updater.dispatcher
        except BaseException as e:
            self.logger.printError(info="TelegramBot Starting-"+str(e),
                                   target="TelegramBot")
        self.dp.add_handler(CommandHandler(command="smt",
                                           callback=self.SendMessage,
                                           pass_args=True))
        self.start_worker()  # Start a worker to do something
        pass

    def SendMessage(self, bot, update, args):
        """
        SendMessage helps the plugin send Events back to the APIManager
        arg1: *args
        arg2: **kwargs
        """
        event = Event(type_ = EType.DEFAULT)
        if args[0] == "hi":
            # print(args[0])
            event.data["targets"] = "CommandLine"
            event.data["content"] = ("hi "+str(update.message.chat_id))
        self.__queue.put(event)  # Put the event to the __queue

    def ReceiveMessage(self, PLUGINS, args, str_list=True):
        """
        ReceiveMessage is the method that's called after API Manager got a message.
        arg1: PLUGINS uses to reflush the list of APIs
        arg2: Args is the message passes into
        arg3: str_list=True. If this method is called by eval, you may leave it True; otherwise, you need to pass False
        """
        if str_list:
            args = list(eval(args))

        if args[0] == "session":
            pass
        self.dp.bot.send_message(chat_id=args[0], text=args[1])
        # Handling the messages
        pass

    def start_worker(self):
        """
        start_worker uses to start the worker
        No need to change anything, unless you need to do so.
        """
        t = threading.Thread(target=self.worker, args=())
        t.setDaemon(True)
        t.start()

    def worker(self):
        """
        Things need to keep running
        """
        self.updater.start_polling()
        # self.updater.idle()
        print("PluginSample Started")
        time.sleep(1)  # Prevent errors from being displayed during initialization
