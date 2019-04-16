import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler,InlineQueryHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineQueryResultVoice
from Smartiome.Core.EventManager import *
from Smartiome.Auxillaries.SystemConf import *
from Smartiome.Auxillaries.UserControl import *
