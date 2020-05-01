# -*- coding: utf-8 -*-
__all__ = ["EncodingTestCase"]
import unittest
from kanjidb import encoding


class EncodingTestCase(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(encoding.decode_unicode("U+4e00"), "一")
        self.assertEqual(encoding.decode_unicode("U4e00"), "一")
        self.assertEqual(encoding.decode_unicode(r"\u4e00"), "一")

    def test_encode(self):
        self.assertEqual(encoding.encode_unicode("一"), "U4e00")
        self.assertEqual(encoding.encode_unicode("一", prefix="U+"), "U+4e00")
        self.assertEqual(encoding.encode_unicode("一", prefix=r"\u"), r"\u4e00")


if __name__ == "__main__":
    unittest.main()
