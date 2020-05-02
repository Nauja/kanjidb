"""This plugin simply load a list of kanjis from external files.
"""
__all__ = ["Plugin"]
import os
from kanjidb.builder.plugins import PluginBase
from kanjidb import encoding, loader


class Plugin(PluginBase):
    def template_config(self):
        return {
            "separator": os.linesep,
            "encoding": encoding.UNICODE_PLUS
        }

    def __call__(self, **kwargs):
        """Load kanjis from `targets` listed in config.
        """
        targets = self.global_config.targets

        kanjis = loader.load(
            *targets,
            encoding=self.plugin_config["encoding"],
            sep=self.plugin_config["separator"]
        )

        kwargs["db"] = {_: {} for _ in kanjis}

        return kwargs
