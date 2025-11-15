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
from pygnition.lumberjack import debug, error, info, stop, warn

# from workshop.projects import Project

CLEAN_PATTERNS = (
    '__pycache__',
    '.ipynb_checkpoints'
)

CLEAN_EXCLUDE = (
    '.git',
    '.venv'
)

class Clean(Driver.Command):
    """Recursively remove annoying build/cache folders in the current project."""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def run(self):
        project_root = self.driver.current_project.path
        removed = []

        for pattern in CLEAN_PATTERNS:
            for folder in project_root.rglob(pattern):
                if not folder.is_dir():
                    continue

                # Skip if folder is inside any excluded directory
                if any(excl in folder.parts for excl in CLEAN_EXCLUDE):
                    continue

                try:
                    shutil.rmtree(folder)
                    removed.append(str(folder))
                except Exception as e:
                    error(f"❌ Failed to remove {folder}: {e}")

        if removed and getattr(self, "verbose", True):
            print("✅ Removed folders:")
            for p in removed:
                print("  ", p)
        else:
            info("No folders matched CLEAN_PATTERNS.")

        return removed