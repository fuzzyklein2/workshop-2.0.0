#!/usr/bin/env python3

from pathlib import Path

from pygnition import *

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

from pygnition.driver import Driver

from workshop.projects import Project

class Compile(Driver.Command):
    def __init__(self, name, line):
        super().__init__(name, line)
        debug(f'Initializing {self.__class__.__name__} object ...')

def __init__(self):
    super().__init__()

def test(self):
    warn(f'{self.name} is under construction!')
    if self.testing: self.dump()

def run(self):
    print(f'Hello, {GLOBE_AMERICA_PICT.strip()} !')
    super().run()

