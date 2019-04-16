from app.PluginLoader import *
from app.plugins import *


def test():
    apis = APIManager()
    print(apis.PLUGINS)
    cmd = input("cmd:")
    plugin = input("plugin:")
    args = []
    arg_num = 0
    apis.cmdRevoke(cmd, plugin, args)

test()
