#!/bin/env python3

import maxthreads


# Lets say you have a function "fun" you want to run within several threads at the same time.

from time import sleep
from threading import active_count
from random import random
def fun():
    print('Active threads: ', active_count())
    sleep(random()*2)

ts = maxthreads.ThreadStarter(max_threads=100)

for i in range(200):
    ts.put(target=fun)