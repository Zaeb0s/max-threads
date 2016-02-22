#!/bin/env python3
import threading


class MaxThreads:
    def __init__(self, max=-1):
        self._max = max
        self._sema = None
        self._limit = False
        if max > -1:
            self._sema = threading.BoundedSemaphore(max)
            self._limit = True

    def start_thread(self, target, args=(), kwargs={}):
        if self._limit:
            self._sema.acquire()
            threading.Thread(target=self._modified_target,
                             args=(self._sema, target, args, kwargs)).start()
        else:
            threading.Thread(target=target,
                             args=args,
                             kwargs=kwargs).start()

    @staticmethod
    def _modified_target(lock, target, args, kwargs):
            try:
                target(*args, **kwargs)
            finally:
                lock.release()

