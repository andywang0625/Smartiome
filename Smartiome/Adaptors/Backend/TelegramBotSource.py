import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from Smartiome.Auxillaries.EventManager import *

class TelegramBotSource:
    def __init__(self, eventManager, type, logger, dp, updater):
        self.logger = logger
        self.dp = dp
        self.__type = type
        self.updater = updater
        self.dp.add_handler(CommandHandler("", self.SendMessage, pass_args = True))
        self.updater.start_polling()
        self.updater.idle()

    def SendMessage(self, bot, update, args):
        event = Event(type_= self.__type)
        #event = Event(type_= "Incoming")

        message = ""
        for word in args:
            message += word
        event.data["Event"] = message
        print(message)
        self.__eventManager.SendEvent(event)
