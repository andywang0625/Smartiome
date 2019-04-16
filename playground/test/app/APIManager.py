class APIManager(object):
    PLUGINS = {}

    def process(self, text, plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                text = self.PLUGINS[plugin_name]().process(text)
        else:
            for plugin_name in plugins:
                text = self.PLUGINS[plugin_name]().process(text)
        return text

    def cmdRevoke(self, cmd, plugin="", args=[]):
        if plugin is ():
            print("No specified plugin")
            return
        else:
            eval("self.PLUGINS[\""+plugin+"\"]()."+cmd+"(self.PLUGINS)")
    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
