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

## Why ?

There already exist various resources one can use to make
learning Japanese easier. For example, you can use the online
dictionary [jisho.org](https://jisho.org/), many websites will teach
you grammar, you can read books, [KanjiVG](https://kanjivg.tagaini.net/) gives a
SVG representation of kanjis, the [Edict Dictionary](http://www.edrdg.org/jmdict/edict.html) and
[Kanjidic2](http://nihongo.monash.edu/kanjidic2/index.html) provide many useful informations on
kanjis, you can find REST API such as [Kanji Alive](https://www.programmableweb.com/api/kanji-alive-rest-api) to query kanjis informations, and [Anki](https://apps.ankiweb.net/) is a great tool to help you remember things (plus you can find
many already made Anki decks for learning Japanese).

But like many people, you may like to learn kanjis and Japanese by learning things you can relate to.
If so you may start to create Anki decks with a subset of words or kanjis you are more interested in, and
this is where you may find it starting difficult to merge informations coming from multiple external resources.

So, KanjiDB is a collection of simple tools that let you work with kanjis, extract informations from external resources,
merge them together, and eventually build something useful for you or others.

## Install

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

## Reading kanjis from file

Create a `sample.yml` file containing:

```
run:
- kanjistream:
    inputs:
    - type: stream
      encoding: unicode_plus
      separator: ";"
      path: kanjis.txt
    outputs:
    - type: stream
      encoding: utf8
      separator: "\n"
      path: "-"
```

Create a `kanjis.txt` file containing unicode encoded kanjis separated by semicolon:

```
U+4E00;U+4E8C
```

Now running `kanjidb build` will output:

```bash
> python -m kanjidb build sample.yml
一
二
```

## Building a database

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
  * `kanjidic2`: produce a JSON dict with data from external Kanjidic2 XML file `kanjidic2.xml` ([download](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project)).
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
