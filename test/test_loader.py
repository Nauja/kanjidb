# -*- coding: utf-8 -*-
__all__ = ["LoaderTestCase"]
import os
import unittest
from kanjidb.encoding import decode_unicode
from kanjidb import loader

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class LoaderTestCase(unittest.TestCase):
    def test_loads(self):
        # UTF8 encoded
        self.assertEqual(loader.loads("一"), ["一"])
        self.assertEqual(loader.loads("一二"), ["一", "二"])
        # With custom separator
        self.assertEqual(loader.loads("一;二", sep=";"), ["一", "二"])
        # Unicode, keep same encoding
        self.assertEqual(loader.loads("U+4E00;U4E8C", sep=";"), ["U+4E00", "U4E8C"])
        # Unicode, convert to UTF8
        self.assertEqual(
            loader.loads("U+4E00;U4E8C", decode=decode_unicode, sep=";"), ["一", "二"]
        )

    def test_load(self):
        # UTF8 encoded
        self.assertEqual(loader.load(KANJIS_UTF8_TXT, sep=";"), ["一", "二"])
        # Unicode
        self.assertEqual(
            loader.load(KANJIS_UNICODE_TXT, decode=decode_unicode, sep=";"),
            ["一", "二"],
        )


if __name__ == "__main__":
    unittest.main()
