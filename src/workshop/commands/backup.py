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

import shutil

from pygnition.driver import Driver
from pygnition.files import File

# from workshop.projects import Project

class Backup(Driver.Command):
    """ Clean the current project and back it up locally.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if self.args:
            self.project = File(self.args[0])
        elif self.driver.current_project:
            self.project = self.driver.current_project
        else: self.project = File(choose_file(directory=True))
        if not self.project:
            info(f'User cancelled backup operation.')
            return
        self.dest_dir = self.driver.user_data / 'backup' / self.project.path.name
        if self.debug: print(f"""Folder to back up: {self.project.path}
Destination directory: {self.dest_dir}
""")

    def run(self):
        result = None

        self.driver.default('clean')
        shutil.copytree(self.project.path,
                        self.dest_dir,
                        dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.git', '.pytest_cache', '.venv')
                       )
        
        return result
