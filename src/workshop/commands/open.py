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
from pygnition.files import File
from pygnition.gui_tools import choose_file
from pygnition.picts import *

from workshop.projects import Project

class Open(Driver.Command):
    """ Open a project by `cd`'ing to its root directory. """
    def __init__(self, name, line, **kwargs):
        super().__init__(name, line, **kwargs)

        # pp(self.args)

        self.log.debug(f'{DEBUG_PICT}Running `{self.cmd_name}`')

    def run(self):
        f = None
        if self.args:
            self.driver.current_project = Project(self.args[0])
        else: f = choose_file(directory=True)
        if f:
            self.driver.current_project = File(f)
            if self.verbose: rp(f"""{INFO_PICT}[cyan bold]Current project[/]:
{str(self.driver.current_project)}
""")
            debug(f'{type(self.driver.current_project)=}')
            # if self.args:
            #     p = Project(self.args[0])
            #     self.driver.current_project = p
            #     self.log.info(f'{INFO_PICT}Opened {p.describe()}')
            # else:
            #     self.log.warning(f'{WARNING_PICT}open command requires an argument.')

