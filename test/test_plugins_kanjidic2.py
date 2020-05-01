# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjidic2TestCase"]
import unittest
from kanjidb import loader
from kanjidb.builder.plugins import kanjidic2


class PluginsKanjidic2TestCase(unittest.TestCase):
    def test(self):
        kanjis = loader.load("data/kanjis_utf8.txt", sep=";")
        db = {_: {} for _ in kanjis}

        plugin = kanjidic2.Kanjidic2Plugin("data/kanjidic2.xml")
        infos = plugin.get_infos("一")
        print(infos)
        plugin(db=db)


if __name__ == "__main__":
    unittest.main()
