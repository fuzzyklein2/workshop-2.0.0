#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️ WARNING! ⚠️ ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PKG_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {str(last_saved_datetime(__file__).date()).split('.')[0]}

## Description

This module defines the Workshop class.

## Typical Use
```python
app = Workshop()
app.run()

Notes
-----
You can include implementation notes, dependencies, or version-specific
details here.

"""

from pygnition.driver import Driver
from pygnition.picts import *
# from pygnition.program import Program
from pygnition.lumberjack import debug, error, info, stop, warn

class Workshop(Driver):

    class Create(Driver.Command):
        def __init__(self, name, line):
            super().__init__(name, line)
            debug('What the fuck?')

        def run(self):
            debug(f'Running {self.cmd_name}')

    class Compile(Driver.Command):
        def __init__(self, name, line):
            super().__init__(name, line)
            debug(f'Initializing {self.__class__.__name__} object ...')


    def __init__(self):
        super().__init__()

    def test(self):
        warn(f'{self.name} is under construction!')
        self.dump()

    def run(self):
        print(f'Hello, {GLOBE_AMERICA_PICT.strip()} !')
        super().run()

if __name__ == '__main__':
    p = Workshop()
    if p.testing:
        p.test()
    p.run()
