# -*- coding: utf-8 -*-

from .utils import load_class, get_logger


class BasePluginManager(object):
    """ Simple plugin manager implementation """

    def __init__(self, logger_verbosity=None):
        self.logger_verbosity = logger_verbosity
        self.log = get_logger(__name__, logger_verbosity)

        self.plugins = []

    def load_plugins(self, plugins):
        """ выполняет загрузку плагинов """

        assert isinstance(plugins, (list, tuple)), "`plugins` should be list"

        for plugin_name in plugins:
            plugin_full_name = 'ereader.{0}'.format(plugin_name)
            plugin_cls = load_class(plugin_full_name)

            plugin_inst = plugin_cls()
            plugin_inst.set_logger(plugin_full_name, self.logger_verbosity)
            self.plugins.append((plugin_name, plugin_inst))

            self.log.debug('Load {0}'.format(plugin_name))

    def configure_plugins(self, config):
        """ выполняет конфигурирование плагинов """

        for name, plugin_inst in self.plugins:
            if not config.has_section(name):
                continue

            plugin_conf = dict(config.items(name))
            plugin_inst.set_config(plugin_conf)

            self.log.debug('Configure {0} with {1}'.format(
                name, plugin_conf))


class BasePlugin(object):
    """ Simple plugin implementation """

    def __init__(self):
        self.log = None
        self.config = {}

    def set_logger(self, name, verbosity=None):
        self.log = get_logger(name, verbosity=verbosity)

    def set_config(self, config):
        assert isinstance(config, dict), "`config` should be dict"

        self.config = config
