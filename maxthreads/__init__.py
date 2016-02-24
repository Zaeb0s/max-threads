#!/bin/env python3

from .maxthreads import *

with open(__path__[0] + '/version', 'r') as r:
    __version__ = r.read()
