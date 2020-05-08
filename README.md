# KanjiDB

[![PyPI version](https://badge.fury.io/py/kanjidb.svg)](https://badge.fury.io/py/kanjidb)
[![Build Status](https://travis-ci.org/Nauja/kanjidb.png?branch=master)](https://travis-ci.org/Nauja/kanjidb)
[![Documentation Status](https://readthedocs.org/projects/kanjidb/badge/?version=latest)](https://kanjidb.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup.svg?style=svg)](https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup)
[![Test Coverage](https://codeclimate.com/github/Nauja/kanjidb/badges/coverage.svg)](https://codeclimate.com/github/Nauja/kanjidb/coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Nauja/kanjidb/issues)

Kanji database builder and REST API.

KanjiDB aims to help you build your own kanji database by compiling
informations from various existing source into a single JSON file.
It's plugin system let you write you own plugin to collect and add new data to kanjis,
or to arrange already written plugins to meet your needs. It's goal
is to be flexible enough to let you export all the informations you
need to build your own app (database, viewer, Anki deck builder, ...) and
progress in learning Japanese. KanjiDB also comes with a REST API allowing to
retrieve those informations and build services uppon.

## Online demo

You can test the REST API online at [kanjidb.jeremymorosi.com/api/v1/doc](http://kanjidb.jeremymorosi.com/api/v1/doc):

![alt text](http://cdn.jeremymorosi.com/kanjidb/swagger_preview.png "Preview")

The documentation is generated by `aiohttp_swagger`.

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

## Generating a JSON database

Create a `kanjis.txt` file containing one UTF-8 encoded kanji per line. This is the list of kanjis
that will be included in our database:

```
一
二
三
```

Now, create a `config.yml` file containing:

```yaml
run:
- kanjidic2:
    kd2_file: path/to/kanjidic2.xml
    inputs:
    - type: stream
      encoding: utf8
      separator: "\n"
      path: path/to/kanjis.txt
    outputs:
    - type: stream
      indent: 4
      path: path/to/db.json
```

In this configuration:
  * **kanjistream**: is a plugin that generate a JSON dict with data from a Kanjidic2 XML file.
  * **path/to/kanjidic2.xml**: is the path to a Kanjidic2 XML file ([download here](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project)).
  * **path/to/kanjis.txt**: is the path to the `kanjis.txt` file.
  * **path/to/db.json**: is the destination of generated JSON database.

Run the following command:

```bash
> python -m kanjidb build config.yml
```

This generate a `db.json` file containing the generated JSON database.
Depending on your configuration this file can be quite big, so here is only an example of what you
would obtain:

```json
{
    "一": {
        "meanings": [{"m_lang": "", "value": "one"}]
    },
    "二": {
        "meanings": [{"m_lang": "", "value": "two"}]
    },
    "三": {
        "meanings": [{"m_lang": "", "value": "three"}]
    }
}
```

You can read more about the `kanjidic2` plugin and its configuration [here](https://kanjidb.readthedocs.io/en/latest/plugins.html#kanjidic2).

## Locally running the REST API

Now we will run a local server with a REST API allowing us to fetch kanjis informations
from generated `db.json` file.

WIP

## Testing

The `test` directory contains many tests that you can run with:

```python
> python setup.py test
```

Or with coverage:

```python
> coverage run --source=kanjidb setup.py test
```
