from gtts import gTTS
from io import BytesIO
from tempfile import TemporaryFile
import playsound
import os
import time
import datetime


class TTSLinstener():
    def __init__(self):
        pass

    def init(self, logger, eventManager, TYPE):
        self.TYPE = TYPE
        self.logger = logger
        self.logger.printInfo("TTSLinstener", "Started")
        tts = gTTS('TTS Linstener Enabled', 'en')
        t = str(int(time.time()))
        tts.save("tmp/"+t+".mp3")
        playsound.playsound("tmp/"+t+".mp3")
        os.remove("tmp/"+t+".mp3")
        del tts
        pass

    def ReadMessage(self, event):
        try:
            tts = gTTS(str(event.data["Event"]), 'en')
            t = str(int(time.time()))
            tts.save("tmp/"+t+".mp3")
            playsound.playsound("tmp/"+t+".mp3")
            os.remove("tmp/"+t+".mp3")
            del tts
        except BaseException as e:
            self.logger.printInfo("TTSLinstener", str(e))
