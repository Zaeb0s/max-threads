#!/bin/env python3

from .maxthreads import MaxThreads

with open(__path__[0] + '/version', 'r') as r:
    __version__ = r.read()

__all__ = ['MaxThreads']

