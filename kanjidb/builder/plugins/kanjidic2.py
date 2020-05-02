"""Use jamdict to load Kanjidic2 XML file.
"""
__all__ = ["load", "Plugin"]
from kanjidb.builder.plugins import PluginBase
try:
    from jamdict.kanjidic2 import Kanjidic2XMLParser
except Exception as e:
    raise Exception("Kanjidic2Plugin requires jamdict to be installed") from e


def load(stream):
    """Load a Kanjidic2 XML file using `jamdict`.

    :param stream: filelike object or filename
    :return: data loaded with `jamdict`.
    """
    parser = Kanjidic2XMLParser()
    if hasattr(stream, "read"):
        return parser.parse_str(stream.read())
    else:
        return parser.parse_file(stream)


class Plugin(PluginBase):
    def template_config(self):
        return {
            "kd2_file": "kd2.xml"
        }

    def configure(self, **kwargs):
        super().configure(**kwargs)

        data = load(self.plugin_config["kd2_file"])
        self._kanjis = {_.literal: _ for _ in data.characters}

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.

        :param db: database
        """
        for kanji, infos in kwargs["db"].items():
            infos.update(self.get_infos(kanji))

    def get_infos(self, kanji):
        """Get infos from Kanjidic2 for a single kanji.

        :param kanji: kanji to retrieve
        :return: dict containing all infos
        """
        data = self._kanjis[kanji]

        return {
            "stroke_count": data.stroke_count,
            "codepoints": [
                {"type": cp.cp_type, "value": cp.value} for cp in data.codepoints
            ],
            "readings": self.get_readings(kanji),
            "meanings": self.get_meanings(kanji),
        }

    def get_readings(self, kanji):
        data = self._kanjis[kanji].rm_groups[0]

        return [_.to_json() for _ in data.readings]

    def get_meanings(self, kanji):
        data = self._kanjis[kanji].rm_groups[0]

        return [_.to_json() for _ in data.meanings]
