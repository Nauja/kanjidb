# -*- coding: utf-8 -*-
__all__ = ["loads", "load"]
import os
import re


def loads(s, decode=None, sep=None):
    '''Load a list of kanjis from string.

    Usage example:

    .. code-block:: python

        >> loader.loads("一二")
        ['一', '二']

    Using custom separator:

    .. code-block:: python

        >> loader.loads("一;二"), sep=";")
        ['一', '二']

    Default behaviour is that kanjis must be UTF8 encoded, but
    this can customized by providing a custom `decode` function:

    .. code-block:: python

        >> loader.loads("\u4E00", decode=encoding.decode_unicode)
        ['一']

    :param s: string to decode
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    '''
    symbols = s if sep is None else s.split(sep)
    symbols = [re.sub("[ \t\r\n]", "", _) for _ in symbols]

    return [
        _ if decode is None else decode(_) for _ in symbols
    ]


def load(*streams, decode=None, sep=None):
    '''Load a list of kanjis from input streams.

    Usage example:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt")

    Using filelike objects:

    .. code-block:: python

        load_kanjis(sys.stdin)

        with open("a.txt", "rb") as f:
            load_kanjis(f)

    Default kanjis separator is the newline character, but this can
    be customized as such:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt", sep=";")

    :param streams: list of input streams to read
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    '''
    sep = sep if sep is not None else os.linesep

    def wrapper():
        for stream in streams:
            # Filelike object
            if hasattr(stream, "read"):
                content = stream.read()
            # Filename
            else:
                with open(stream, "rb") as f:
                    content = f.read().decode()

            yield from loads(content, decode=decode, sep=sep)

    return list(wrapper())
