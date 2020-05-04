# -*- coding: utf-8 -*-
__all__ = ["load_plugin_modules"]
import pkgutil
import importlib
import pkg_resources
import functools
import kanjidb.builder.plugins


def load_plugin_modules(names):
    names = ["kanjidb.builder.plugins.{}".format(_) for _ in names]

    def iter_namespace(ns_pkg):
        for finder, name, ispkg in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
            yield name, functools.partial(importlib.import_module, name)
        for _ in pkg_resources.iter_entry_points("kanjidb.builder.plugins"):
            yield "kanjidb.builder.plugins.{}".format(_.name), _.load

    def normalize(name):
        return name[name.rfind(".") + 1 :]

    return {
        normalize(name): load()
        for name, load in iter_namespace(kanjidb.builder.plugins)
        if name in names
    }
