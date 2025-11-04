#!/usr/bin/env python3

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

COMMON_LICENSES = [
    "MIT License",
    "GNU GPL v3",
    "Apache License 2.0",
    "BSD 3-Clause",
    "BSD 2-Clause",
    "Mozilla Public License 2.0",
    "Unlicense",
    "Proprietary / Custom",
]

KEY_PROMPTS = [
    ('name', 'Project Name:'),
    ('version', 'Version:'),
    ('author', 'Author:'),
    ('type', 'Project Type:'),
    ('description', 'Description:'),
    ('requirements', 'Requirements:'),
    ('github', 'GitHub Repository:'),
    ('license', 'License:')
]
