__all__ = ["PluginBase"]
from abc import ABC, abstractmethod


class PluginBase(ABC):
    def template_config(self):
        '''Return the template config for this plugin.

        :return: a dict containing template config
        '''
        return {}

    def configure(self, *, global_config, plugin_config):
        '''Configure this plugin.

        :param global_config: global builder configuration
        :param plugin_config: plugin configuration
        '''
        self.global_config = global_config
        self.plugin_config = plugin_config

    @abstractmethod
    def __call__(self, **kwargs):
        '''Execute this plugin.

        :param kwargs: inputs
        :return: outputs
        '''
        raise NotImplementedError()
