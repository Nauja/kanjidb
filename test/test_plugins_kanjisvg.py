# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjiSVGTestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.plugins import kanjidic2, kanjisvg

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIDIC2_XML = os.path.join(DATA_DIR, "kanjidic2.xml")
SVG_INPUT_DIR = os.path.join(DATA_DIR, "svg")
SVG_OUTPUT_DIR = os.path.join(SVG_INPUT_DIR, "output")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_kanjisvg.yml")
BASE_URL = "http://127.0.0.1:8080/svg/"


class PluginsKanjiSVGTestCase(unittest.TestCase):
    @staticmethod
    def generate_db():
        return kanjidic2.run(
            inputs=[{
                "type": "stream",
                "separator": ";",
                "path": KANJIS_UTF8_TXT
            }],
            kd2_file=KANJIDIC2_XML
        )

    def test_plugin(self):
        plugin = kanjisvg.Plugin()
        config = plugin.required_config
        config.update(
            {
                "inputs": [{"type": "var", "name": "db"}],
                "outputs": [{"type": "var", "name": "db"}],
                "svg_input_dir": SVG_INPUT_DIR,
                "svg_output_dir": SVG_OUTPUT_DIR,
                "base_url": BASE_URL
            }
        )
        plugin.configure(global_config={}, plugin_config=config)

        result = plugin(db=PluginsKanjiSVGTestCase.generate_db())
        db = result["db"]
        self.assertTrue("media" in db["一"], "Invalid result")
        self.assertTrue("svg" in db["一"]["media"], "Invalid result")

    def test_run(self):
        db = kanjisvg.run(
            inputs=[{"type": "var", "name": "db"}],
            outputs=[{"type": "var", "name": "db"}],
            svg_input_dir=SVG_INPUT_DIR,
            svg_output_dir=SVG_OUTPUT_DIR,
            base_url=BASE_URL,
            kwargs={"db": PluginsKanjiSVGTestCase.generate_db()}
        )

        self.assertTrue("media" in db["一"], "Invalid result")
        self.assertTrue("svg" in db["一"]["media"], "Invalid result")

    def test_sample(self):
        builder.main([SAMPLE_TXT])


if __name__ == "__main__":
    unittest.main()
