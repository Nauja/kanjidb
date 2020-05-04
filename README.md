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
steps that will run for building the database. Start by creating a file named `config.yml` looking like this:

```yaml
run:
- kanjistream:
    encoding: unicode_plus
    separator: ";"
    in: "-"
    out: kanjis
- kanjidic2:
    kd2_file: kanjidic2.xml
    in: kanjis
    out: db
- jsonwriter:
    encoding: unicode_plus
    indent: 4
    in: db
    out:
    - db.json
    - "-"
```

Each step listed in `run` correspond to a plugin located in `kanjidb.builder.plugins` and
can have its own configuration. You can arrange plugins as you want and even run them
multiple times.

In this configuration:
  * `kanjistream`: read kanjis from `sys.stdin`.
  * `kanjidic2`: produce a JSON dict with data from external Kanjidic2 XML file `kanjidic2.xml` ([download](http://www.edrdg.org/kanjidic/kanjidic2.xml.gz)).
  * `jsonwriter`: write the JSON dict to `db.json` and `sys.stdout`.

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

As described in configuration, KanjiDB simply produced a JSON dict containing
Kanjidic2 data for the two kanjis from `sys.stdin`. It also created a file
called `db.json` containing this JSON dict.

This example give you a glimpse of how KanjiDB works and how you can assemble
its plugins to output useful data on kanjis.

http://www.edrdg.org/wiki/index.php/KANJIDIC_Project
