__all__ = ["Plugin", "run", "load"]
from kanjidb.builder.plugins import PluginBase, kanjistream

try:
    from jamdict.kanjidic2 import Kanjidic2XMLParser
except Exception as e:
    raise Exception("kanjidic2 requires jamdict to be installed") from e


class Plugin(PluginBase):
    """This plugin load kanjis data from an external Kanjidic2 XML file.

    Kanjidic2 XML file is parsed using `jamdict`.
    """

    @property
    def template_config(self):
        return {
            "inputs": [{"type": "var", "name": "kanjis"}],
            "output": {"type": "var", "name": "db"},
            "kd2_file": "kd2.xml",
        }

    @property
    def required_config(self):
        return self.template_config

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.
        """
        run(
            inputs=self.plugin_config["inputs"],
            output=self.plugin_config["output"],
            kd2_file=self.plugin_config["kd2_file"],
            kwargs=kwargs,
        )

        return kwargs

    def __repr__(self):
        return "Kanjidic2"


def run(inputs, output, *, kd2_file, kwargs=None):
    kwargs = kwargs if kwargs is not None else {}

    # Read kanjis to generate
    kanjistream.run(
        inputs=inputs, outputs=[{"type": "var", "name": output["name"]}], kwargs=kwargs
    )

    kanjis = kwargs[output["name"]]

    # Load external Kanjidic2 XML file
    data = load(kd2_file)
    data = {_.literal: _ for _ in data.characters}

    # Merge infos with kanjis
    kwargs[output["name"]] = {_: data[_].to_json() for _ in kanjis}


def load(stream):
    """Load a Kanjidic2 XML file using `jamdict`.

    :param stream: filelike object or filename
    :return: data loaded with `jamdict`.
    """
    parser = Kanjidic2XMLParser()
    if hasattr(stream, "read"):
        return parser.parse_str(stream.read())
    else:
        return parser.parse_file(stream)
