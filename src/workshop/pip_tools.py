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

from pygnition._data_tools import is_valid_data_line

def read_requirements():
    """Read requirements.txt or .in, ignoring comments and blanks."""
    for filename in ("requirements.txt", "requirements.in"):
        p = Path(filename)
        if p.exists():
            lines = p.read_text().splitlines()
            return "\n".join(
                s for s in lines if is_valid_data_line(s)
            )
    return ""
