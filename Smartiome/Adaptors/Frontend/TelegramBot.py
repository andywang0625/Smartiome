import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from Smartiome.Core.EventManager import *
from Smartiome.Auxillaries.SystemConf import *
from Smartiome.Auxillaries.UserControl import *
from Smartiome.Auxillaries.SystemManager import *
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
        # self.start_worker()  # Start a worker to do something
        pass

    def SendMessage(self, bot, update, args):
        """
        SendMessage helps the plugin send Events back to the APIManager
        arg1: *args
        arg2: **kwargs
        """
        event = Event(type_ = EType.DEFAULT)
        event.data["source"] = "TelegramBot"
        if args[0] == "hi":
            # print(args[0])
            event.data["target"] = "CommandLine"
            event.data["content"] = ("hi "+str(update.message.chat_id))
        elif args[0] == "-revoke":
            event.data["target"] = "revoke"
            event.data["cmd"] = args[1]
            event.data["plugin"] = args[2]
            event.data["args"] = args[3]

        elif args[0] == "-sys":
            event.data["target"] = "SystemManager"
            event.data["recipient"] = str(update.message.chat_id)
            event.data["content"] = args[1]
            pass
        elif args[0] == "self":
            event.data["target"] = "TelegramBot"
            event.data["recipient"] = str(update.message.chat_id)
            event.data["content"] = str(update.message.chat_id)

        elif args[0] == "-event":
            event.data["target"] = args[1]
            if args[2] == "self":
                event.data["recipient"] = str(update.message.chat_id)
            else:
                event.data["recipient"] = args[2]
            num = 0
            event.data["content"] = ""
            for word in args:
                if num < 3:
                    num += 1
                    continue
                event.data["content"] += word+" "
                # event.data["chat_id"] = str(update.message.chat_id)
        self.__queue.put(event)  # Put the event to the __queue

    def ReceiveMessage(self, PLUGINS, event=None, str_list=False):
        """
        ReceiveMessage is the method that's called after API Manager got a message.
        arg1: PLUGINS uses to reflush the list of APIs
        arg2: Args is the message passes into
        arg3: str_list=True. If this method is called by eval, you may leave it True; otherwise, you need to pass False
        """

        if event:
            # print("called")
            if str_list:
                event = Event(eval(event))
        try:
            self.dp.bot.send_message(chat_id=int(event.data["recipient"]),
                                     text=str(event.data["content"]))
        except:
            self.logger.printError("ReceiveMessage"
                                   ,target="TelegramBot")
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

    def test(self):
        print("Hello")

    def worker(self):
        """
        Things need to keep running
        """
        self.updater.start_polling()
        # self.updater.idle()
        print("PluginSample Started")
        time.sleep(1)  # Prevent errors from being displayed during initialization
