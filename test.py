#!/bin/env python3

import maxthreads

from time import sleep
from random import random
import threading

def w():
    print(threading.active_count())
    for i in range(10000000):
        x = 2
    # sleep(random()*2)

x = maxthreads.MaxThreads()
for i in range(200):
    x.start_thread(target=w)

