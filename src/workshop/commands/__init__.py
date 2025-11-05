#!/usr/bin/env python3

from importlib import import_module

from pygnition._auto_doc import auto_class_doc, auto_doc, AUTO_DOC_HEAD
from pygnition._imports import import_chain

PACKAGE_NAME = import_chain()[0]

try:
    _metadata = import_module(f'{PACKAGE_NAME}._metadata')
    globals().update(vars(_metadata))
except ModuleNotFoundError: # Most likely happens in a Jupyter notebook or a console
                            # Appears to happen in pydoc as well.
    from .._metadata import *

__doc__ = f"""The 🔥  pygnition 🔥  package sets up an environment for any script that imports it.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

## Author

{AUTHOR}

## Date

{LAST_SAVED_DATE}

## Usage

```python
from pygnition.program import Program
Program().run()

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.

## [GitHub]({get_upstream_url()})

"""

import importlib
import pkgutil
from pathlib import Path

COMMANDS = {}

# Import all modules in this package
package_dir = Path(__file__).parent
for _, module_name, is_pkg in pkgutil.iter_modules([str(package_dir)]):
    if is_pkg:
        continue

    module = importlib.import_module(f"{__name__}.{module_name}")

    # Register all classes named "Command" or subclasses thereof
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type):
            # Check if it has "Command" as a base somewhere
            for base in attr.__mro__:
                if base.__name__ == "Command":
                    COMMANDS[attr.__name__.lower()] = attr
                    break
