from Smartiome.Auxillaries.EventManager import *
from socket import *
import threading
import pickle


class CType(object):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
