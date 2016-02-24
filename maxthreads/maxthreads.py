#!/bin/env python3
import threading
from queue import Queue, Empty


class MaxThreads:
    def __init__(self, max_threads=-1, thread_timeout=2):
        self._queue = Queue()
        self._thread_timeout = thread_timeout

        self._threads_active = 0
        self._threads_waiting = 0

        self._max_threads = max_threads

        if max_threads > 0:
            self._limit = True
        else:
            self._limit = False

    def start_thread(self, target, args=(), kwargs={}):
        self._queue.put((target, args, kwargs))
        if (self._threads_active < self._max_threads or not self._limit) and self._threads_waiting == 0:
            self._threads_active += 1
            threading.Thread(target=self._loop).start()

    def _loop(self):
        serve = True
        try:
            while serve:
                try:
                    self._threads_waiting += 1
                    target, args, kwargs = self._queue.get(timeout=self._thread_timeout)
                    self._threads_waiting -= 1
                except Empty:
                    self._threads_waiting -= 1
                    serve = False
                else:
                    target(*args, **kwargs)
        except:
            self._threads_active += 1
            threading.Thread(target=self._loop).start()
            raise
        finally:
            self._threads_active -= 1

    def threads_active(self):
        return self._threads_active

    def threads_waiting(self):
        return self._threads_active

    def empty_queue(self):
        try:
            while True:
                self._queue.get()
        except Empty:
            pass
