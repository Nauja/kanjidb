__all__ = ["build", "main"]
from kanjidb.builder.configuration import Configuration


def build(config):
    """Build a kanji database.

    :param config: builder configuration
    :return: build result
    """
    kwargs = {}

    for step in config.run:
        print(step)
        new_kwargs = step(**kwargs)

        if new_kwargs is not None:
            kwargs = new_kwargs

    return kwargs


def main(argv):
    import argparse

    parser = argparse.ArgumentParser(prog="KanjiDB", description="Kanji Database")
    parser.add_argument("--config", nargs="?", help="YAML configuration file")
    parser.add_argument("-o", "--output", nargs="?", help="Output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    parser.add_argument("targets", nargs="+", help="Files containing kanjis")
    args = parser.parse_args(argv)

    config = Configuration(
        targets=args.targets, output=args.output, verbose=args.verbose
    )
    config.load(args.config, default=args.config)

    build(config)
