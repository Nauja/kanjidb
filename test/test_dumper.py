# -*- coding: utf-8 -*-
__all__ = ["DumperTestCase"]
import sys
import unittest
from kanjidb.encoding import encode_unicode
from kanjidb import dumper


class DumperTestCase(unittest.TestCase):
    def test_dumps(self):
        db = {"一": {}, "二": {}}
        print(dumper.dumps(db))
        print(dumper.dumps(db, encode=encode_unicode))

    def test_dump(self):
        db = {"一": {}, "二": {}}
        dumper.dump(db, sys.stdout)
        dumper.dump(db, sys.stdout, encode=encode_unicode)


if __name__ == "__main__":
    unittest.main()
