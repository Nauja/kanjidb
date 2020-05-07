
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
`Kanjidic2 <http://www.edrdg.org/wiki/index.php/KANJIDIC_Project>`_ provide many useful informations on
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

Usage
-----

Start by creating a ``helloworld.yml`` file containing:

.. code-block:: yaml

   run:
   - helloworld: {}

This YAML configuration file serves to describe and configure a series of steps that will
be run by the ``kanjidb build`` command. Each step listed in ``run`` correspond to a `plugin <https://kanjidb.readthedocs.io/en/latest/plugins.html>`_ located in ``kanjidb.builder.plugins``.
A plugin is a simple function you can use and configure from the YAML configuration
file. Here we tell that we will run a single step with the plugin `helloworld <https://kanjidb.readthedocs.io/en/latest/plugins.html#helloworld>`_\ , which only output "今日わ" to ``sys.stdout``.

Now, run the following command:

.. code-block:: bash

   > python -m kanjidb build helloworld.yml
   今日わ

This is how you can use KanjiDB to work with kanjis.
Some plugins allow to read kanjis from inputs while others are dedicated to
combine informations from external resources. Take a look at the `documentation <https://kanjidb.readthedocs.io/>`_
for a full list of builtin plugins.

But you are not limited to scripting the build process with a YAML configuration file.
For instance, here is how you would obtain the same result with a Python script:

.. code-block:: python

   > from kanjidb.builder.plugins import helloworld
   > helloworld.run()
   今日わ

This option has the advantages of being a more powerful and versatile way of using KanjiDB.
It even allows you to write custom plugins to code new features, but it requires to write and distribute Python scripts.

Generating a JSON database
--------------------------

Create a ``kanjis.txt`` file containing one UTF-8 encoded kanji per line. This is the list of kanjis
that will be included in our database:

.. code-block::

   一
   二
   三

Now, create a ``config.yml`` file containing:

.. code-block:: yaml

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

In this configuration:


* **kanjistream**\ : is a plugin that generate a JSON dict with data from a Kanjidic2 XML file.
* **path/to/kanjidic2.xml**\ : is the path to a Kanjidic2 XML file (\ `download here <http://www.edrdg.org/wiki/index.php/KANJIDIC_Project>`_\ ).
* **path/to/kanjis.txt**\ : is the path to the ``kanjis.txt`` file.
* **path/to/db.json**\ : is the destination of generated JSON database.

Run the following command:

.. code-block:: bash

   > python -m kanjidb build config.yml

This generate a ``db.json`` file containing the generated JSON database.
Depending on your configuration this file can be quite big, so here is only an example of what you
would obtain:

.. code-block:: json

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

You can read more about the ``kanjidic2`` plugin and its configuration `here <https://kanjidb.readthedocs.io/en/latest/plugins.html#kanjidic2>`_.

Running a REST API
------------------

Now we will run a local server with a REST API allowing us to fetch kanjis informations
from generated ``db.json`` file.

WIP

Running samples
---------------

In the ``test.data`` directory you will find many sample configuration files that you can run with
``kanjidb builder``. For example, you can run ``sample_helloworld.yml`` with following command:

.. code-block:: python

   > python -m kanjidb build test/data/sample_helloworld.yml
   今日わ

Don't hesitate to take a look at samples as it's a good way to learn how to use KanjiDB.

Testing
-------

The ``test`` directory contains many tests that you can run with:

.. code-block:: python

   > python setup.py test

Or with coverage:

.. code-block:: python

   > coverage run --source=kanjidb setup.py test
