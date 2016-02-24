#!/bin/env python3
import maxthreads


# Lets say you have a function "fun" you want to run within several threads at the same time.

from time import sleep
from threading import active_count
from random import random


def fun():
    # print('Active threads: ', active_count())
    # print('In queue: ', thread_limiter._queue._qsize())
    counter.i += 1
    sleep(random()*2)


# The following initiates a MaxThreads object with the limit set to 10
thread_limiter = maxthreads.MaxThreads(10)
class counter:
    i = 0
# The following starts 200 threads each running the fun function.
for i in range(100):
    thread_limiter.start_thread(target=fun)

# from queue import Queue
# import threading
# x = Queue()
#
# def p():
#     return x.get()
#
# threading.Thread(target=p).start()
#
# x.put('hello')
# for i in range(20):
#     y = 1
# print(x.empty())