#!/usr/bin/env python3

import os
from pathlib import Path

PKG_CONFIG_FILE = Path(os.curdir) / 'etc/packages.txt'
assert(PKG_CONFIG_FILE.exists())
print(' '.join(PKG_CONFIG_FILE.read_text().strip().split('\n')))