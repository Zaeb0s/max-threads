#!/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import maxthreads


# Lets say you have a function "fun" you want to run within several threads at the same time.
from time import sleep
from threading import active_count
from random import random


def fun():
    print('Active threads: ', active_count())
    sleep(random())


# The following initiates a MaxThreads object with the limit set to 3
thread_limiter = maxthreads.MaxThreads(30, thread_timeout=10)

# The following starts 10 threads each running the fun function.
for i in range(10):
    thread_limiter.add_task(target=fun)

while thread_limiter.get_task_queue_count() != 0:
    pass
else:
    print('All tasks done')
    thread_limiter.stop()
