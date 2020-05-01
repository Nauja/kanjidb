# kanjidb
wip

Show help:

```
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

```
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
