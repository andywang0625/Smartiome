from gtts import gTTS
from io import BytesIO
from tempfile import TemporaryFile
import playsound
import os
import time
import datetime


class TTSLinstener:
    def __init__(self, logger):
        self.logger = logger
        logger.printInfo("TTSLinstener", "Started")
        tts = gTTS('TTS Linstener Enabled', 'en')
        t = str(int(time.time()))
        tts.save("tmp/"+t+".mp3")
        playsound.playsound("tmp/"+t+".mp3")
        os.remove("tmp/"+t+".mp3")
        del tts
        pass

    def ReadMessage(self, event):
        tts = gTTS(str(event.data["Event"]), 'en')
        t = str(int(time.time()))
        tts.save("tmp/"+t+".mp3")
        playsound.playsound("tmp/"+t+".mp3")
        os.remove("tmp/"+t+".mp3")
        del tts
