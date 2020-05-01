__all__ = ["build", "main"]
import os
import sys
import json
import functools
from kanjidb import loader, dumper, encoding
from kanjidb.builder.plugins import kanjidic2


def build(
    kanjis,
    *,
    plugins=None,
    output=None,
    decode=None,
    encode=None,
    indent=None,
    verbose=None
):
    """Build a JSON kanji database.

    :param kanjis: list of kanjis to build or callable
    :param plugins: plugins used to build database
    :param output: output file or callable
    :param decode: how to decode input kanjis
    :param encode: how to encode output kanjis
    :param verbose: verbosity level
    """
    # Load
    if hasattr(kanjis, "__call__"):
        kanjis = kanjis()

    if decode:
        kanjis = [decode(_) for _ in kanjis]

    # Transform
    db = {k: {} for k in kanjis}
    for _ in plugins:
        _(db=db, verbose=verbose)

    # Dump
    if hasattr(output, "__call__"):
        output(db=db, verbose=verbose)
    else:
        dumper.dump(db, output=output, encode=encode, indent=indent)


def main(argv):
    import argparse

    parser = argparse.ArgumentParser(prog="KanjiDB", description="Kanji Database")
    parser.add_argument("--kd2-file", nargs="?", help="Kanjidic2 XML file")
    parser.add_argument("-o", "--output", nargs="?", help="Output file")
    parser.add_argument("--sep", nargs="?", help="Separator between kanjis")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    parser.add_argument("targets", nargs="*", help="Files containing kanjis")
    args = parser.parse_args(argv)

    build(
        kanjis=loader.load(*args.targets, sep=args.sep)
        if args.targets
        else loader.load(sys.stdin, decode=encoding.decode_unicode, sep=args.sep),
        plugins=[kanjidic2.Kanjidic2Plugin(args.kd2_file)],
        output=args.output,
        encode=encoding.encode_unicode,
        verbose=args.verbose,
    )
