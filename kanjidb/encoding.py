# -*- coding: utf-8 -*-
__all__ = ["get_codepoint", "decode_unicode", "encode_unicode"]
import re


def get_codepoint(kanji):
    return kanji.encode("unicode_escape")[2:].decode().lower()


def decode_unicode(s):
    '''Decode an unicode encoded kanji.

    Input string may be in following formats:

    ..code-block:: python

        >> decode_unicode("U+4E00")
        "一"

        >> decode_unicode("U4E00")
        "一"

        >> decode_unicode("\\u4E00")
        "一"

    :param s: unicode character to decode
    :return: decoded character
    '''
    m = re.match("^(?:\\\\[uU]|[uU][+]?)([0-9a-fA-F]+)$", s)
    if not m:
        raise Exception("Invalid unicode string \"{}\"".format(s))

    return chr(int(m.group(1).upper(), 16))


def encode_unicode(s, *, prefix=None):
    '''Encode an UTF8 kanji to unicode.

    Usage examples:

    ..code-block:: python

        >> encode_unicode("一")
        "U4e00"

        >> decode_unicode("一", prefix="U+")
        "U+4e00"

        >> decode_unicode("一", prefix="\\u")
        "\u4e00"

    :param s: UTF8 character to encode
    :return: encoded character
    '''
    prefix = prefix if prefix is not None else "U"

    return "{}{}".format(prefix, get_codepoint(s))
