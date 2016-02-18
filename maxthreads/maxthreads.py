#!/bin/env python3

import threading


class MaxThreads:
    def __init__(self, max_threads):
        self.sema = threading.BoundedSemaphore(max_threads)

    def start_thread(self, target, args=(), kwargs={}):
        self.sema.acquire()
        threading.Thread(target=self._target_modifier,
                         args=(target, args, kwargs)).start()

    def _target_modifier(self, target, args=(), kwargs={}):
        try:
            target(*args, **kwargs)
        finally:
            self.sema.release()


if __name__ == '__main__':
    from time import sleep
    from random import random

    def w():
        print(threading.active_count())
        sleep(random()*2)

    x = MaxThreads(1)
    for i in range(200):
        x.start_thread(w)
