#!/usr/bin/env python3

from pygnition._initools import AUTHOR, DESCRIPTION, last_saved_datetime, PKG_NAME, REQUIREMENTS

from ._version import VERSION

__doc__ = f"""The 🛠️  {PKG_NAME} 🛠️  program is a test run for the 🔥  pygnition 🔥  project.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

## Author

{AUTHOR}

## Usage

`$ python -m {PKG_NAME} [OPTIONS] [ARGUMENTS]`

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.
"""
