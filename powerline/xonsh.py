"""
Xonsh Shell Support 

This will override the default shell in xonsh, and set powerline to 
build the prompt. Since 
"""
from __future__ import unicode_literals, absolute_import, division, print_function

# Powerline Specific Libs
from powerline import Powerline
from powerline.lib.dict import mergedicts
from powerline.lib.unicode import strings

# Xonsh Specific Libs, and LazyModule evaluvation
from sys import modules as _modules
from types import ModuleType as _ModuleType
from importlib import import_module as _import_module


class _LazyModule(_ModuleType):

    def __init__(self, pkg, mod, asname=None):
        '''Lazy module 'pkg.mod' in package 'pkg'.'''
        self.__dct__ = {
            'loaded': False,
            'pkg': pkg,  # pkg
            'mod': mod,  # pkg.mod
            'asname': asname,  # alias
            }

    @classmethod
    def load(cls, pkg, mod, asname=None):
        if mod in _modules:
            key = pkg if asname is None else mod
            return _modules[key]
        else:
            return cls(pkg, mod, asname)

    def __getattribute__(self, name):
        if name == '__dct__':
            return super(_LazyModule, self).__getattribute__(name)
        dct = self.__dct__
        mod = dct['mod']
        if dct['loaded']:
            m = _modules[mod]
        else:
            m = _import_module(mod)
            glbs = globals()
            pkg = dct['pkg']
            asname = dct['asname']
            if asname is None:
                glbs[pkg] = m = _modules[pkg]
            else:
                glbs[asname] = m
            dct['loaded'] = True
        return getattr(m, name)


class XonshPowerline(Powerline):
    """
    TODO: Add input args for the extentions if needed. 
    """
    def init(self, **kwargs):
          super(XonshPowerline, self).init(ext="xonsh", render_module="xonsh", **kwargs)

