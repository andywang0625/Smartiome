from Smartiome.Core.APIManager import *
import threading
import time


@APIManager.plugin_register("PluginSample")
class PluginSample(threading.Thread):
    def __init__(self, __queue, eventManager=None):
        super().__init__(self)
        self.eventManager = eventManager  # Allows Plugins send event
        self.__queue = __queue  # Allows APIManager Receive Messages
        self.start_worker(self)  # Start a worker to do something
        pass

    def SendMessage(self, *args, **kwargs):
        """
        SendMessage helps the plugin send Events back to the APIManager
        arg1: *args
        arg2: **kwargs
        """
        event = Event(type_ = EType.DEFAULT)
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

        # Handling the messages
        pass

    def start_worker(self):
        """
        start_worker uses to start the worker
        No need to change anything, unless you need to do so.
        """
        t = threading.Thread(target=self.worker, args=(self,))
        t.setDaemon(True)
        t.start()

    def worker(self):
        """
        Things need to keep running
        """
        print("CommandLine Started")
        time.sleep(1)
        while True:
            time.sleep(0.3)
            self.SendMessage(self)
