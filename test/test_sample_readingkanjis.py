# -*- coding: utf-8 -*-
__all__ = ["SampleReadingKanjisTestCase"]
import os
import unittest
from kanjidb import builder

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_readingkanjis.yml")


class SampleReadingKanjisTestCase(unittest.TestCase):
    def test(self):
        builder.main([SAMPLE_TXT])


if __name__ == "__main__":
    unittest.main()
