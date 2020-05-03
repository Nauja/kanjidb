"""This plugin simply save database to an external JSON file.
"""
__all__ = ["Plugin", "dumps", "dump"]
import sys
import os
import json
import functools
from kanjidb.builder.plugins import PluginBase
import kanjidb.encoding


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {
            "encoding": kanjidb.encoding.UNICODE_PLUS,
            "indent": 4
        }

    @property
    def required_config(self):
        config = self.template_config
        config.update({
            "in": "db",
            "out": "-"
        })

        return config

    def __call__(self, **kwargs):
        db = kwargs[self.plugin_config["in"]]

        dump(
            db,
            output=self.plugin_config["out"],
            encoding=self.plugin_config["encoding"],
            indent=self.plugin_config["indent"]
        )

        print("Saved to {}".format(self.plugin_config["out"]))

    def __repr__(self):
        return "JSONWriter"


def dumps(db, *, encoding=None, encode=None, indent=None):
    """Dump the JSON database.

    Parameter `output` may be a `str` or `filelike` object:

    .. code-block:: python

        # Create and write to "foo.json" file
        with open("foo.json", "wb+") as f:
            save_db(f, db=db)

        # Create and write to "foo.json" file
        save_db("foo.json", db=db)

        # Write to sys.stdout
        save_db(sys.stdout, db=db)

    Parameter `output` may be omitted to print to `sys.stdout`:

    .. code-block:: python

        save_db(db=db)

    Parameter `dumps` can be provided to customize how db is printed:

    .. code-block:: python

        save_db(db=db, dumps=json.dumps)

    :param db: database
    """
    encode = encode if encode is not None else functools.partial(
        kanjidb.encoding.encode,
        encoding=encoding
    )

    indent = indent if indent is not None else 4

    if encode:
        db = {encode(k): v for k, v in db.items()}

    return json.dumps(db, indent=indent, ensure_ascii=False)


def dump(db, output=None, *, encoding=None, encode=None, indent=None):
    """Dump the JSON database.

    Parameter `output` may be a `str` or `filelike` object:

    .. code-block:: python

        # Create and write to "foo.json" file
        with open("foo.json", "wb+") as f:
            save_db(f, db=db)

        # Create and write to "foo.json" file
        save_db("foo.json", db=db)

        # Write to sys.stdout
        save_db(sys.stdout, db=db)

    Parameter `output` may be omitted to print to `sys.stdout`:

    .. code-block:: python

        save_db(db=db)

    Parameter `dumps` can be provided to customize how db is printed:

    .. code-block:: python

        save_db(db=db, dumps=json.dumps)

    :param output: output file
    :param db: JSON database
    :param indent: JSON indent level
    :param dumps: dumps JSON database
    :param verbose: verbosity level
    """
    output = output if output is not None else sys.stdout

    content = dumps(db, encoding=encoding, encode=encode, indent=indent)

    if output == "-":
        output = sys.stdout

    # Filelike object
    if hasattr(output, "write"):
        output.write(content)
    # For filename
    elif isinstance(output, str):
        parent = os.path.dirname(output)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(output, "wb+") as f:
            f.write(content.encode())
    # Unknown output type
    else:
        raise Exception("output expected to be str, filelike or callable")
