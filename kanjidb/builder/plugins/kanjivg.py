__all__ = ["Plugin", "load"]
import os
from kanjidb.builder.plugins import PluginBase
from kanjidb import encoding


class Plugin(PluginBase):
    """This plugin add vectorial drawing of kanjis to JSON dict.
    """

    @property
    def template_config(self):
        return {"sources": "vectorials/"}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"in": "db"})

        return config

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.

        :param db: database
        """
        db = kwargs[self.plugin_config["in"]]

        for kanji, data in db.items():
            cp = encoding.get_codepoint(kanji)
            if len(cp) < 5:
                cp = "0{}".format(cp)
            filename = "{}.svg".format(cp)

            data["vectorial"] = filename if os.path.isfile(
                os.path.join(self.plugin_config["sources"], filename)
            ) else None

    def __repr__(self):
        return "KanjiVG"
