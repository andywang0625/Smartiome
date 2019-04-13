import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from Smartiome.Auxillaries.EventManager import *
from Smartiome.Adaptors.Controller.SystemManager import *
from Smartiome.Auxillaries.SystemConf import *
from Smartiome.Auxillaries.UserControl import *
from Smartiome.Adaptors.Controller.ControllerHelper import *

class TelegramBotSource:
    def __init__(self, eventManager, type, logger, dp, updater):
        self.__eventManager = eventManager
        self.logger = logger
        self.dp = dp
        self.__type = type
        self.updater = updater
        self.updater.dispatcher.add_handler(CommandHandler("smt", self.SendMessage, pass_args = True))
        self.updater.start_polling()
        self.updater.idle()

    def SendMessage(self, bot, update, args):
        #Broadcast Command
        if auth(update):
            try:
                args[0]
                message = ""
                try:
                    if args[0] == "-b":
                        num = 0
                        for word in args:
                            if num == 0:
                                num += 1
                                continue
                            message += (word+" ")
                            num += 1
                        event = Event(type_ = EType.BROADCAST)
                        event.data["Event"] = message
                        event.data["ChatId"] = update.message.chat_id
                        self.__eventManager.SendEvent(event)
                        return
                except BaseException as e:
                    self.logger.printError("Broadcast "+str(e)+"-", target="TelegramBotSource")
                    event = Event(type_ = EType.OUTPUT)
                    event.data["Event"] = "Nothing to Broadcast"
                    event.data["ChatId"] = update.message.chat_id
                    self.__eventManager.SendEvent(event)
                    return
            except BaseException as e:
                event = Event(type_ = EType.OUTPUT)
                event.data["Event"] = "try -help or ? to see which controllers are running."
                event.data["ChatId"] = update.message.chat_id
                self.__eventManager.SendEvent(event)
                return

            #Register Controllers
            RegisteredControllers = [
                ["SystemManager", "system"],
                ["ControllerHelper", "chelper"],
            ]
            system = SystemManager(self.logger, self.__eventManager)
            chelper = ControllerHelper(self.logger, self.__eventManager, RegisteredControllers)

            try:
                args[0]
                command = ""
                for word in args:
                    command += (word+" ").lower()
                if "(update)" not in command:
                    command += "(update)"
                eval(command)

            except BaseException as e:
                self.logger.printError("Getting Info", target="TelegramBotSource")
                event = Event(type_ = EType.OUTPUT)
                event.data["Event"] = "Failed to run command: "+command
                event.data["ChatId"] = update.message.chat_id
                self.__eventManager.SendEvent(event)
