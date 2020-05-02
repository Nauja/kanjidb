WIP

# KanjiDB

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Kanji database builder and REST API.

KanjiDB aims to help you build your own kanji database by gathering
informations from various existing source. It's plugin system let you
write you own plugin to collect and add new data to kanjis,
or to arrange already written plugins to meet your needs. It's goal
is to be flexible enough to let you export all the informations you
need to build your own app (database, viewer, Anki deck builder, ...) and
progress in learning Japanese. KanjiDB also comes with a REST API allowing to
retrieve those informations and built services uppon.

# How to use

Show help:

```bash
> python -m kanjidb

Usage:  kanjidb COMMAND [OPTIONS]

A kanji database accessible via REST API

Options:
  -v, --version            Print version information and quit

Commands:
  build       Build kanji database from sources
  run         Run local server and REST API

Run 'kanjidb COMMAND --help' for more information on a command.

```

Build kanji database from Kanjidic2 XML file:

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
