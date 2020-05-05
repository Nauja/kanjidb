
KanjiDB
=======


.. image:: https://badge.fury.io/py/kanjidb.svg
   :target: https://badge.fury.io/py/kanjidb
   :alt: PyPI version


.. image:: https://travis-ci.org/Nauja/kanjidb.png?branch=master
   :target: https://travis-ci.org/Nauja/kanjidb
   :alt: Build Status


.. image:: https://readthedocs.org/projects/kanjidb/badge/?version=latest
   :target: https://kanjidb.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup.svg?style=svg
   :target: https://circleci.com/gh/Nauja/kanjidb/tree/circleci-project-setup
   :alt: CircleCI


.. image:: https://codeclimate.com/github/Nauja/kanjidb/badges/coverage.svg
   :target: https://codeclimate.com/github/Nauja/kanjidb/coverage
   :alt: Test Coverage


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black


.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/Nauja/kanjidb/issues
   :alt: contributions welcome


Kanji database builder and REST API.

KanjiDB aims to help you build your own kanji database by gathering
informations from various existing source. It's plugin system let you
write you own plugin to collect and add new data to kanjis,
or to arrange already written plugins to meet your needs. It's goal
is to be flexible enough to let you export all the informations you
need to build your own app (database, viewer, Anki deck builder, ...) and
progress in learning Japanese. KanjiDB also comes with a REST API allowing to
retrieve those informations and build services uppon.

Why ?
-----

There already exist various resources one can use to make
learning Japanese easier. For example, you can use the online
dictionary `jisho.org <https://jisho.org/>`_\ , many websites will teach
you grammar, you can read books, `KanjiVG <https://kanjivg.tagaini.net/>`_ gives a
SVG representation of kanjis, the `Edict Dictionary <http://www.edrdg.org/jmdict/edict.html>`_ and
`Kanjidic2 <http://nihongo.monash.edu/kanjidic2/index.html>`_ provide many useful informations on
kanjis, you can find REST API such as `Kanji Alive <https://www.programmableweb.com/api/kanji-alive-rest-api>`_ to query kanjis informations, and `Anki <https://apps.ankiweb.net/>`_ is a great tool to help you remember things (plus you can find
many already made Anki decks for learning Japanese).

But like many people, you may like to learn kanjis and Japanese by learning things you can relate to.
If so you may start to create Anki decks with a subset of words or kanjis you are more interested in, and
this is where you may find it starting difficult to merge informations coming from multiple external resources.

So, KanjiDB is a collection of simple tools that let you work with kanjis, extract informations from external resources,
merge them together, and eventually build something useful for you or others.

Install
-------

Using pip:

.. code-block:: bash

   > pip install kanjidb

Show help:

.. code-block:: bash

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

Reading kanjis from file
------------------------

Create a ``sample.yml`` file containing:

.. code-block::

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

Create a ``kanjis.txt`` file containing unicode encoded kanjis separated by semicolon:

.. code-block::

   U+4E00;U+4E8C

Now running ``kanjidb build`` will output one UTF-8 encoded kanji per line:

.. code-block:: bash

   > python -m kanjidb build sample.yml
   一
   二

Equivalent in Python:

.. code-block:: python

   from kanjidb.encoding import UNICODE_PLUS, UTF8
   from kanjidb.builder.plugins import kanjistream

   kanjistream.run(
       inputs=[{
           "type": "stream",
           "encoding": UNICODE_PLUS,
           "separator": ";",
           "path": "kanjis.txt"
       }],
       outputs=[{
           "type": "stream",
           "encoding": UTF8,
           "separator": "\n",
           "path": "-"
       }]
   )

Building a database
-------------------

The command ``kanjidb build`` requires a YAML configuration file describing all
steps that will run for building the database. Start by creating a file named ``config.yml`` looking like this:

.. code-block:: yaml

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

Each step listed in ``run`` correspond to a plugin located in ``kanjidb.builder.plugins`` and
can have its own configuration. You can arrange plugins as you want and even run them
multiple times.

In this configuration:


* ``kanjistream``\ : read kanjis from ``sys.stdin``.
* `kanjidic2`: produce a JSON dict with data from external Kanjidic2 XML file `kanjidic2.xml` ([download](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project)).
* ``jsonwriter``\ : write the JSON dict to ``db.json`` and ``sys.stdout``.

Now running ``kanjidb build`` will produce following output:

.. code-block:: bash

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

As described in configuration, KanjiDB simply produced a JSON dict containing
Kanjidic2 data for the two kanjis from ``sys.stdin``. It also created a file
called ``db.json`` containing this JSON dict.

This example give you a glimpse of how KanjiDB works and how you can assemble
its plugins to output useful data on kanjis.

http://www.edrdg.org/wiki/index.php/KANJIDIC_Project
