__all__ = ["Plugin", "load"]
import os
import shutil
from kanjidb.builder.plugins import PluginBase, jsonstream
from kanjidb import encoding


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {"svg_dir": "svg/",
            "inputs": [{"type": "var", "name": "db"}],
            "outputs": [{"type": "var", "name": "db"}]
        }

    @property
    def required_config(self):
        return self.template_config

    def __call__(self, **kwargs):
        run(inputs=self.plugin_config["inputs"], outputs=self.plugin_config["outputs"],
            svg_input_dir=self.plugin_config["svg_input_dir"],
            svg_output_dir=self.plugin_config["svg_output_dir"],
            base_url=self.plugin_config["base_url"], kwargs=kwargs)

        return kwargs

    def __repr__(self):
        return "KanjiSVG"


def run(inputs, outputs=None, *, svg_input_dir, svg_output_dir, base_url, kwargs=None):
    """Add SVG representation of kanjis to database.

    Given a directory containing:

    .. code-block::

        - 04e00.svg
        - 04e8c.svg
        - ...

    And a JSON kanji database such as:

    .. code-block:: python

        {
            "04e00": {...},
            "04e8c": {...}
        }

    This plugin inject SVG URLs into database:

    .. code-block:: python

        {
            "04e00": {
                "media": {
                    "svg": "base_url/04e00.svg"
                },
                ...
            },
            "04e8c": {
                "media": {
                    "svg": "base_url/04e8c.svg"
                },
                ...
            }
        }

    SVG files corresponding to kanjis present in database are
    copied to `svg_output_dir`.

    Configuration:

    .. code-block:: yaml

        run:
        - kanjisvg:
          svg_input_dir: string
          svg_output_dir: string
          base_url: string
          inputs:
          - type: stream|var
            [separator: string] # stream only
            [encoding: string] # stream only
            [path: string] # stream only
            [name: string] # var only
          outputs:
          - type: stream|var
            [path: string] # stream only
            [indent: int] # stream only
            [name: string] # var only

    Combine with `kanjidic2`:

    .. code-block:: yaml

        run:
        - kanjidic2:
            kd2_file: path/to/kanjidic2.xml
            inputs:
            - type: stream
              encoding: utf8
              separator: "\\n"
              path: "-"
            outputs:
            - type: var
              name: result
        - kanjisvg:
            svg_input_dir: path/to/svgs/
            svg_output_dir: path/to/cdn/
            base_url: http://cdn.com/
            inputs:
            - type: var
              name: result
            outputs:
            - type: stream
              indent: 4
              path: path/to/db.json

    :param inputs: input streams
    :param output: output streams
    :param svg_input_dir: directory containing SVG files
    :param svg_output_dir: where to copy SVG files
    :param base_url: base URL to access SVG files
    :param kwargs: context
    :return: a JSON object with kanjis data
    """
    outputs = outputs if outputs is not None else []
    kwargs = kwargs if kwargs is not None else {}

    os.makedirs(svg_output_dir, exist_ok=True)

    # Read db
    db = jsonstream.run(inputs=inputs, kwargs=kwargs)

    # Add SVG data
    for kanji, data in db.items():
        filename = get_svg_filename(svg_input_dir, kanji)

        media = data.setdefault("media", {})
        media["svg"] = None

        if os.path.isfile(filename):
            basename = os.path.basename(filename)

            shutil.copy(
                filename,
                os.path.join(svg_output_dir, basename)
            )

            media["svg"] = base_url + basename

    # Write to output streams
    jsonstream.run(
        inputs=[{"type": "var", "name": "db"}],
        outputs=outputs,
        kwargs={"db": db},
    )

    # Store to variables
    for _ in outputs:
        if _["type"] == "var":
            kwargs[_["name"]] = db

    return db


def get_svg_filename(svg_dir, kanji):
    cp = encoding.get_codepoint(kanji)
    if len(cp) < 5:
        cp = "0{}".format(cp)

    return os.path.join(svg_dir, "{}.svg".format(cp))
