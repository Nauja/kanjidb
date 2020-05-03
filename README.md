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

# Build database

Building a database is done by executing multiple steps described in
a YAML configuration file. KanjiDB will create a default `config.yaml`
file if an existing configuration doesn't exist or none is provided.
This default configuration file looks like this:

```yaml
run:
- kanjiloader:
    encoding: unicode_plus
    separator: "\r\n"
- kanjidic2:
    kd2_file: kd2.xml
- dbexporter:
    encoding: unicode_plus
    indent: 4
```

It's all the steps that KanjiDB will run to build the database.
Each step correspond to a plugin located in `kanjidb.builder.plugins` and
can have its own configuration.

```bash
> echo "U4E00;U4E8D" | python -m kanjidb build \
  --sep ";" \
  --kd2-file /path/to/kanjidic2.xml
{
    "U4e00": {
        "stroke_count": 1,
        "codepoints": [
            {
                "type": "ucs",
                "value": "4e00"
            },
            {
                "type": "jis208",
                "value": "16-76"
            }
        ],
        "readings": [
            {
                "type": "pinyin",
                "value": "yi1",
                "on_type": "",
                "r_status": ""
...
```

http://www.edrdg.org/wiki/index.php/KANJIDIC_Project
