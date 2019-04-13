from Smartiome.Auxillaries.SystemConf import *
from telegram.ext import Updater


def auth(update):
    if SystemConf.PERMISSION == "masteronly" and str(update.message.chat_id) == SystemConf.MASTER:
        return True
    elif SystemConf.PERMISSION == "public":
        return True
    elif SystemConf.PERMISSION == "auth":
        if update.message.chat_id == SystemConf.MASTER:
            return True
        else:
            pass
    update.message.reply_text("Permission Denied")
    return False
