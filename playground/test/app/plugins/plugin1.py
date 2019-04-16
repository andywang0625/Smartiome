from ..PluginLoader import APIManager


@APIManager.plugin_register('plugin1')
class Plugin1(object):
    def revokeprocess(self, PLUGINS):
        return PLUGINS["plugin2"]().process()
