# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjiStreamTestCase"]
import os
import unittest
from kanjidb.builder.plugins import kanjistream
from kanjidb.encoding import UNICODE_PLUS

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class PluginsKanjiStreamTestCase(unittest.TestCase):
    def test_plugin(self):
        """Running via Plugin interface.
        """
        plugin = kanjistream.Plugin()
        config = plugin.required_config
        config.update(
            {
                "inputs": [
                    {
                        "type": "stream",
                        "encoding": UNICODE_PLUS,
                        "separator": ";",
                        "path": KANJIS_UNICODE_TXT,
                    }
                ],
                "outputs": [{"type": "var", "name": "kanjis"}],
            }
        )

        plugin.configure(global_config={}, plugin_config=config)

        result = plugin()
        self.assertTrue("kanjis" in result, "Invalid output")
        kanjis = result["kanjis"]
        self.assertEqual(kanjis, ["一", "二"], "Invalid result")

    def test_run(self):
        """Running via code.
        """
        kwargs = {}

        # Read file and store to "result"
        kanjistream.run(
            inputs=[
                {
                    "type": "stream",
                    "encoding": UNICODE_PLUS,
                    "separator": ";",
                    "path": KANJIS_UNICODE_TXT,
                }
            ],
            outputs=[{"type": "var", "name": "result"}],
            kwargs=kwargs,
        )

        self.assertTrue("result" in kwargs, "Invalid output")
        self.assertEqual(kwargs["result"], ["一", "二"], "Invalid result")

        # Get "result" and write to stdout
        kanjistream.run(
            inputs=[{"type": "var", "name": "result"}],
            outputs=[
                {
                    "type": "stream",
                    "encoding": UNICODE_PLUS,
                    "separator": ";",
                    "path": "-",
                }
            ],
            kwargs=kwargs,
        )

    def test_loads(self):
        # UTF8 encoded
        self.assertEqual(kanjistream.loads("一"), ["一"])
        self.assertEqual(kanjistream.loads("一二"), ["一", "二"])
        # With custom separator
        self.assertEqual(kanjistream.loads("一;二", sep=";"), ["一", "二"])
        # Unicode, keep same encoding
        self.assertEqual(
            kanjistream.loads("U+4E00;U4E8C", sep=";"), ["U+4E00", "U4E8C"]
        )
        # Unicode, convert to UTF8
        self.assertEqual(
            kanjistream.loads("U+4E00;U4E8C", encoding=UNICODE_PLUS, sep=";"),
            ["一", "二"],
        )

    def test_load(self):
        # UTF8 encoded
        self.assertEqual(kanjistream.load(KANJIS_UTF8_TXT, sep=";"), ["一", "二"])
        # Unicode
        self.assertEqual(
            kanjistream.load(KANJIS_UNICODE_TXT, encoding=UNICODE_PLUS, sep=";"),
            ["一", "二"],
        )

    def test_dump(self):
        kanjistream.dump(["一", "二"], "-", encoding=UNICODE_PLUS, sep=";")


if __name__ == "__main__":
    unittest.main()
