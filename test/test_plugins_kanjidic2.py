# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjidic2TestCase"]
import os
import unittest
from kanjidb import loader
from kanjidb.builder.plugins import kanjidic2

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIDIC2_XML = os.path.join(DATA_DIR, "kanjidic2.xml")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")


class PluginsKanjidic2TestCase(unittest.TestCase):
    def test(self):
        kanjis = loader.load(KANJIS_UTF8_TXT, sep=";")
        db = {_: {} for _ in kanjis}

        plugin = kanjidic2.Plugin()
        plugin.configure(
            global_config={},
            plugin_config={
                "kd2_file": KANJIDIC2_XML
            }
        )
        infos = plugin.get_infos("一")
        print(infos)
        plugin(db=db)


if __name__ == "__main__":
    unittest.main()
