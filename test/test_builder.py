# -*- coding: utf-8 -*-
__all__ = ["BuilderTestCase"]
import sys
import os
import unittest
from kanjidb import encoding, loader, builder
from kanjidb.builder.plugins import kanjidic2

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIDIC2_XML = os.path.join(DATA_DIR, "kanjidic2.xml")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class BuilderTestCase(unittest.TestCase):
    def test_build(self):
        builder.build(
            kanjis=loader.load(KANJIS_UNICODE_TXT, sep=";"),
            plugins=[kanjidic2.Kanjidic2Plugin(KANJIDIC2_XML)],
            decode=encoding.decode_unicode,
            output=sys.stdout,
            verbose=True,
        )


if __name__ == "__main__":
    unittest.main()
