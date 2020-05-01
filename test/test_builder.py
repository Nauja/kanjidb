# -*- coding: utf-8 -*-
__all__ = ["BuilderTestCase"]
import sys
import unittest
from kanjidb import encoding, loader, builder
from kanjidb.builder.plugins import kanjidic2


class BuilderTestCase(unittest.TestCase):
    def test_build(self):
        builder.build(
            kanjis=loader.load(
                "data/kanjis_unicode.txt",
                sep=";"
            ),
            plugins=[
                kanjidic2.Kanjidic2Plugin("data/kanjidic2.xml")
            ],
            decode=encoding.decode_unicode,
            output=sys.stdout,
            verbose=True
        )


if __name__ == "__main__":
    unittest.main()
