# -*- coding: utf-8 -*-
__all__ = ["SampleReadingKanjisTestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.configuration import Configuration

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_readingkanjis.yml")


class SampleReadingKanjisTestCase(unittest.TestCase):
    def test(self):
        config = Configuration()
        config.load(SAMPLE_TXT)

        result = builder.build(config)

        self.assertTrue("kanjis" in result, "Invalid output")
        kanjis = result["kanjis"]
        self.assertEqual(kanjis, ["一", "二"], "Invalid result")


if __name__ == "__main__":
    unittest.main()
