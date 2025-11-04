#!/usr/bin/env python3

from .startmeup import *

from pathlib import Path

MODULE_NAME = Path(__file__).stem

__doc__ = f"""A concise summary of what this module does.

:module: {PACKAGE_NAME}.{MODULE_NAME}
:version: {VERSION}
:author: {AUTHOR}
:date: {last_saved_datetime(__file__)}

## Description

Instantiates a Workshop object and calls its `run` function.

## Typical Use

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

"""

from .workshop import Workshop

if __name__ == '__main__':
    # breakpoint()
    app = Workshop()
    # app.dump()
    Workshop().run()
