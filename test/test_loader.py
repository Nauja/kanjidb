# -*- coding: utf-8 -*-
__all__ = ["LoaderTestCase"]
import unittest
from kanjidb.encoding import decode_unicode
from kanjidb import loader


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
        self.assertEqual(loader.loads("U+4E00;U4E8C", decode=decode_unicode, sep=";"), ["一", "二"])

    def test_load(self):
        # UTF8 encoded
        self.assertEqual(loader.load("data/kanjis_utf8.txt", sep=";"), ["一", "二"])
        # Unicode
        self.assertEqual(loader.load("data/kanjis_unicode.txt", decode=decode_unicode, sep=";"), ["一", "二"])


if __name__ == "__main__":
    unittest.main()
