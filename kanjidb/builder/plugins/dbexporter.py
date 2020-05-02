"""This plugin simply save database to an external JSON file.
"""
__all__ = ["Plugin"]
from kanjidb.builder.plugins import PluginBase
from kanjidb import encoding, dumper


class Plugin(PluginBase):
    def template_config(self):
        return {
            "encoding": encoding.UNICODE_PLUS,
            "indent": 4
        }

    def __call__(self, **kwargs):
        dumper.dump(
            kwargs["db"],
            output=self.global_config.output,
            encoding=self.plugin_config["encoding"],
            indent=self.plugin_config["indent"]
        )

        print("Saved to {}".format(self.global_config.output))
