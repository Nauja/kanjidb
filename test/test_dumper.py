# -*- coding: utf-8 -*-
__all__ = ["DumperTestCase"]
import sys
import unittest
from kanjidb.encoding import UNICODE_PLUS
from kanjidb import dumper

UTF8_OUTPUT = """{
"一": {},
"二": {}
}"""

UNICODE_OUTPUT = """{
"U+4e00": {},
"U+4e8c": {}
}"""


class DumperTestCase(unittest.TestCase):
    def test_dumps(self):
        db = {"一": {}, "二": {}}
        self.assertEqual(
            dumper.dumps(db, indent=0),
            UTF8_OUTPUT
        )
        self.assertEqual(
            dumper.dumps(db, encoding=UNICODE_PLUS, indent=0),
            UNICODE_OUTPUT
        )

    def test_dump(self):
        db = {"一": {}, "二": {}}
        dumper.dump(db, sys.stdout)
        dumper.dump(db, sys.stdout, encoding=UNICODE_PLUS)


if __name__ == "__main__":
    unittest.main()
