from Smartiome.Core.APIManager import *
import threading
import time


"""
You may need to change all PluginSample to your own plugin's name
"""


@APIManager.plugin_register("PluginSample")
class PluginSample:
    def __init__(self, __queue, logger, eventManager=None):
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue  # Allows APIManager Receive Messages
        self.logger = logger
        pass

    def SendMessage(self, *args, **kwargs):
        """
        SendMessage helps the plugin send Events back to the APIManager
        arg1: *args
        arg2: **kwargs
        """

        """
        Generic Message Format:
            data["target"]: str(plugin_name)
            data["source"]: str(plugin_name)
            (opt)data["recipient"]: str(recipient_id)
            data["content"]: list(content or command)
        """

        event = Event(type_ = EType.DEFAULT)
        self.__queue.put(event)  # Put the event to the __queue

    def ReceiveMessage(self, PLUGINS, event=None, str_list=False):
        """
        ReceiveMessage is the method that's called after API Manager got a message.
        arg1: PLUGINS uses to reflush the list of APIs
        arg2: Args is the message passes into
        arg3: str_list=True. If this method is called by eval, you may leave it True; otherwise, you need to pass False
        """
        if str_list:
            event = object(eval(event))

        # Handling the messages
        pass

    def start_worker(self):
        """
        start_worker uses to start the worker
        No need to change anything, unless you need to do so.
        """
        t = threading.Thread(target=self.worker, args=())
        t.setDaemon(True)

        # You may not need to start it as a Controller
        # t.start()

    def worker(self):
        """
        Things need to keep running
        """
        print("PluginSample Started")
        time.sleep(1)  # Prevent errors from being displayed during initialization
        while True:
            time.sleep(0.3)  # Prevent errors from being displayed during running
            self.SendMessage(self) # Calling SendMessage
