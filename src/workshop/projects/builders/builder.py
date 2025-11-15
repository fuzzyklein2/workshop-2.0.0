#!/usr/bin/env python3

from pathlib import Path

from ...startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PACKAGE_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {LAST_SAVED_DATE}

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

## [GitHub]({get_upstream_url()})

"""

from enum import auto, Enum
from pprint import pformat

from pygnition.lumberjack import debug, error, info, stop, warn
from pygnition.picts import *
from pygnition.tools import cd, cwd

@auto_class_doc()
class Builder():
    """A superclass for C project builders."""

    BUILDER_TYPE_STRS = [
        'cpp', 'make', 'cmake', 'meson'
    ]

    class Types(Enum):
        CPP = auto()
        MAKE = auto()
        CMAKE = auto()
        MESON = auto()

    # ──────────────────────────────────────────────
    # Subclass registry and auto-dispatch
    # ──────────────────────────────────────────────
    _registry: dict[str, type[Project]] = {}

    # @auto_doc
    @classmethod
    def register(cls, name: str):
        """
        Decorator for subclasses to self-register under a type name.
        Example:
            @Builder.register("make")
            class MakeBuilder(Builder): ...
        """
        def decorator(subclass):
            cls._registry[name] = subclass
            # print(f'Added {name} : {subclass} to Project registry.')
            return subclass
        return decorator

    def __new__(cls, p):
        """Return the proper subclass (Script, Program, etc.) if detected."""
        if cls is not Builder:
            # Already constructing a subclass — skip re-dispatch
            return super().__new__(cls)

        # path = Path(p)
        try:
            print(f'Constructing {cls}')
            builder_type = cls.detect_type(p)
            subclass = cls._registry.get(builder_type, cls)
            print(f'Subclass: {subclass}')
            # if subclass is not cls:
            return subclass.__new__(subclass, p)
        except Exception as e:
            pass
            print(f"DEBUG: Error instantiating Builder object: {e}")

        return super().__new__(cls)

    # ──────────────────────────────────────────────
    # Normal Builder initialization
    # ──────────────────────────────────────────────
    def __init__(self, p):
        super().__init__()
        print(f"{DEBUG_PICT}Builder.__init__ called for {p}")
        self.project = p
        self.directory = self.project.path
        self.std = 20
        self.cmd_lines = list()
        self.cwd = cwd()
        self.exe_path = f'bin/{self.project.name}'
        # self.src_files = self.project.source.rglob('*')
        self.src_files = [
            p for p in self.project.source.rglob('*')
            if ".ipynb_checkpoints" not in p.parts
        ]
        print()
        info(f"""Source files:
{pformat(self.src_files)}
""")

    def compile(self):
        error("Can't call `compile` from `Builder` base class!")

    def finish(self):
        cd(self.cwd)
        
    @staticmethod
    def detect_type(p # Should be a CppProject but that annotation could lead to circular imports.
                   ) -> str: # String that specifies the build tool.
        """ Just looks for Makefiles. Nothing fancy. """
        if type(p) is str: p = Path(p)
        if type(p) is not Path: p = p.path
        ls = p.glob('*')

        if 'mexon.build' in ls:
            return 'meson'
        elif 'CMakeLists.txt' in ls:
            return 'cmake'
        elif 'Makefile' in ls:
            return 'make'
        return 'cpp'

def build(self):
    cd(self.directory)
    self.compile()
    self.finish()
