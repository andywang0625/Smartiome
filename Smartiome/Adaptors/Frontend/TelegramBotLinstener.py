from telegram.ext import Updater, Dispatcher
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from telegram.utils.helpers import escape_markdown
import json


class TelegramBotLinstener:
    def __init__(self, logger, dp, updater):
        #self.logger = logger
        #self.logger.printInfo("TelegramBotLinstener", "Started")
        self.updater = updater
        self.dp = dp

    def testStart(self, event):
        self.dp.add_handler(CommandHandler("hi", self.hi(self.dp.bot, saying=event.data["Event"])))
        self.updater.start_polling()
        self.updater.idle()

    def talkToMaster(self, event):
        if event.data["Event"] != "":
            self.dp.bot.send_message(chat_id="409297171", text=event.data["Event"])
        else:
            self.dp.bot.send_message(chat_id="409297171", text="Message is Empty")

    def talkTo(self, event):
        try:
            event.data["ChatId"]
            chatId = event.data["ChatId"]
        except:
            chatId = "409297171" #send to master

        if event.data["Event"] != "":
            self.dp.bot.send_message(chat_id=chatId, text=event.data["Event"])
        else:
            self.dp.bot.send_message(chat_id=chatId, text="Message is Empty")

def TelegramBotInit(API, logger) -> Dispatcher:
    try:
        updater = Updater(API)
        dp = updater.dispatcher
        return dp, updater
    except BaseException as e:
        logger.printError("Init TelegramBotInit", e)
