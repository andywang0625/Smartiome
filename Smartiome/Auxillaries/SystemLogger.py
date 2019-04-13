import logging
from Smartiome.Auxillaries.SystemLogger import *


class SystemLogger:
    def __init__(self, level=logging.INFO):
        logging.basicConfig(format='%(asctime)-15s - %(levelname)s - %(target)-s - %(message)s', level=level)
        self.logger = logging.getLogger('Smartiome')

    def printInfo(self, title, Command="", target="Smartiome"):
        self.logger.info(title+ ' %s ', 'whoiam', extra={'target':target})

    def printError(self, action="action", info="", target="Smartiome"):
        self.logger.error( action+' Failed: %s', info, extra={'target':target})
