from ..PluginLoader import APIManager

@APIManager.plugin_register("plugin2")
class Plugin2(object):
    def process(self):
        print("success")
