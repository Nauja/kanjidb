# -*- coding: utf-8 -*-
__all__ = ["load_plugin_modules"]
import sys
import os
import re
import functools
import kanjidb.encoding


def load_plugin_modules(names):
    import pkgutil
    import importlib
    import kanjidb.builder.plugins
    names = ["kanjidb.builder.plugins.{}".format(_) for _ in names]

    def iter_namespace(ns_pkg):
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    def normalize(name):
        return name[name.rfind('.')+1:]

    return {
        normalize(name): importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(kanjidb.builder.plugins)
        if name in names
    }
