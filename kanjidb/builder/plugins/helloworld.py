# -*- coding: utf-8 -*-
__all__ = ["Plugin", "run"]
from kanjidb.builder.plugins import PluginBase, kanjistream
import kanjidb.encoding


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {}

    @property
    def required_config(self):
        return {
            "output": {
                "type": "stream",
                "encoding": kanjidb.encoding.UTF8,
                "path": "-"
            }
        }

    def __call__(self, **kwargs):
        run(self.plugin_config["output"])

        return kwargs

    def __repr__(self):
        return "HelloWorld"


def run(output):
    if output["type"] == "stream":
        output["separator"] = ""

    kanjistream.run(
        inputs=[{
            "type": "var",
            "name": "kanjis"
        }],
        outputs=[output],
        kwargs={
            "kanjis": "今日わ"
        }
    )
