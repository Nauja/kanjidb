# -*- coding: utf-8 -*-
__all__ = ["PluginsHelloWorldTestCase"]
import unittest
from kanjidb.builder.plugins import helloworld
import kanjidb.encoding


class PluginsHelloWorldTestCase(unittest.TestCase):
    def test_plugin(self):
        """Running via Plugin interface.
        """
        plugin = helloworld.Plugin()
        config = plugin.required_config
        config.update(
            {
                "output": {
                    "type": "stream",
                    "encoding": kanjidb.encoding.UNICODE_ESCAPE,
                    "path": "-",
                }
            }
        )

        plugin.configure(global_config={}, plugin_config=config)

        plugin()

    def test_run(self):
        """Running via code.
        """
        helloworld.run(
            output={"type": "stream", "encoding": kanjidb.encoding.UTF8, "path": "-"}
        )


if __name__ == "__main__":
    unittest.main()
