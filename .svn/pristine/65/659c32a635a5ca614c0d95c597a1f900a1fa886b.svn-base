#!/usr/bin/python
# -*- coding: utf-8 -*-

from .common import run, runex
from .common import adduser, deluser
from .common import PathConverter, Env, Service, Hosts

import sys
if sys.platform == "win32":
    from .win32 import *
elif sys.platform == "linux":
    from .linux import *
else:
    raise