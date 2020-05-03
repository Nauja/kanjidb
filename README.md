WIP

# KanjiDB

[![PyPI version](https://badge.fury.io/py/kanjidb.svg)](https://badge.fury.io/py/kanjidb)
[![Build Status](https://travis-ci.org/Nauja/kanjidb.png?branch=master)](https://travis-ci.org/Nauja/kanjidb)
[![CircleCI](https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup.svg?style=svg)](https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup)
[![Test Coverage](https://codeclimate.com/github/Nauja/kanjidb/badges/coverage.svg)](https://codeclimate.com/github/Nauja/kanjidb/coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Nauja/kanjidb/issues)

Kanji database builder and REST API.

KanjiDB aims to help you build your own kanji database by gathering
informations from various existing source. It's plugin system let you
write you own plugin to collect and add new data to kanjis,
or to arrange already written plugins to meet your needs. It's goal
is to be flexible enough to let you export all the informations you
need to build your own app (database, viewer, Anki deck builder, ...) and
progress in learning Japanese. KanjiDB also comes with a REST API allowing to
retrieve those informations and build services uppon.

# Install

Using pip:

```bash
> pip install kanjidb
```

Show help:

```bash
> python -m kanjidb -h

Usage:  kanjidb COMMAND [OPTIONS]

A kanji database accessible via REST API

Options:
  -v, --version            Print version information and quit
  -h, --help               Show this help

Commands:
  build       Build kanji database from sources
  run         Run local server and REST API

Run 'kanjidb COMMAND --help' for more information on a command.

```

# Building a database

The command `kanjidb build` requires a YAML configuration file describing all
steps to run for building a database. Start by creating a file named `config.yml`
and looking like this:

```yaml
run:
- kanjistream:
    encoding: unicode_plus
    separator: ";"
- kanjidic2:
    kd2_file: kanjidic2.xml
- jsonwriter:
    encoding: unicode_plus
    indent: 4
```

Each step listed in `run` correspond to a plugin located in `kanjidb.builder.plugins` and
can have its own configuration. You can arrange plugins as you want and even run them
multiple times.

Now running `kanjidb build` will produce following output:

```bash
> echo "U4E00;U4E8D" | python -m kanjidb build config.yml
{
    "U+4e00": {
        ...
        "meanings": [
            {
                "m_lang": "",
                "value": "one"
            },
        ...
        ]
    },
    "U+4e8d": {
        ...
        "meanings": [
            {
                "m_lang": "",
                "value": "to take small steps"
            },
            ...
        ]
    }
}
```

Here KanjiDB simply read two kanjis from `stdin` and produced a JSON dict containing
informations on these kanjis.

This example give you a glimpse of how KanjiDB works and how you can assemble
its plugins to output useful informations on kanjis.

http://www.edrdg.org/wiki/index.php/KANJIDIC_Project
