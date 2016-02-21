#!/bin/env python3
import threading


class MaxThreads:
    def __init__(self, max=-1):
        self._max = max

        self._sema = None
        self._limit = False
        if max > 0:
            self._sema = threading.BoundedSemaphore(max)
            self._limit = True

    def start_thread(self, target, args=(), kwargs={}):
        if self._limit:
            modified_target = self._modify_target(target)
            self._sema.acquire()
        else:
            modified_target = target

        threading.Thread(target=modified_target,
                         args=args,
                         kwargs=kwargs).start()

    def _modify_target(self, target):
        def new_function(*args, **kwargs):
            try:
                target(*args, **kwargs)
            finally:
                self._sema.release()
        return new_function




