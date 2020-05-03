# -*- coding: utf-8 -*-
__all__ = ["JSONWriterTestCase"]
import sys
import unittest
from kanjidb.encoding import UNICODE_PLUS
from kanjidb.builder.plugins import jsonwriter

UTF8_OUTPUT = """{
"一": {},
"二": {}
}"""

UNICODE_OUTPUT = """{
"U+4e00": {},
"U+4e8c": {}
}"""


class JSONWriterTestCase(unittest.TestCase):
    def test_dumps(self):
        db = {"一": {}, "二": {}}
        self.assertEqual(
            jsonwriter.dumps(db, indent=0),
            UTF8_OUTPUT
        )
        self.assertEqual(
            jsonwriter.dumps(db, encoding=UNICODE_PLUS, indent=0),
            UNICODE_OUTPUT
        )

    def test_dump(self):
        db = {"一": {}, "二": {}}
        jsonwriter.dump(db, sys.stdout)
        jsonwriter.dump(db, sys.stdout, encoding=UNICODE_PLUS)


if __name__ == "__main__":
    unittest.main()
