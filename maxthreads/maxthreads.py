#!/bin/env python3
import threading
from queue import Queue, Empty
from loopfunction import Loop


class MaxThreads:
    def __init__(self, max_threads=-1):
        self._sema = None
        self._limit = False
        if max_threads > -1:
            self._sema = threading.BoundedSemaphore(max_threads)
            self._limit = True

    def start_thread(self, target, args=(), kwargs={}):
        if self._limit:
            self._sema.acquire()
            thread = threading.Thread(target=self._modified_target,
                                      args=(self._sema, target, args, kwargs))
        else:
            thread = threading.Thread(target=target,
                                      args=args,
                                      kwargs=kwargs)
        thread.start()
        return thread

    @staticmethod
    def _modified_target(lock, target, args, kwargs):
            try:
                target(*args, **kwargs)
            finally:
                lock.release()


class ThreadStarter:
    """This class can run a separate thread for the sole purpose of starting threads with MaxThreads (yeah, I know
    very specific, but I found myself implementing this or something similar in most programs using MaxThreads)
    This can be useful if we want to queue up functions to be started in a subthread from a thread that we don't
    want to be blocked by the MaxThreads object.

    The put funtion puts functions in a queue to be started by MaxThreads.start_thread

    execute_queue
    """
    def __init__(self, max_threads=-1):
        self._ḿaxthreads = MaxThreads(max_threads)
        self._queue = Queue()
        self._loop = Loop(target=self._main_loop)

    def serve_forever(self, subthread=True):
        self._loop.start(subthread=subthread)

    def stop_serve_forever(self):
        self._loop.stop()

    def _execute_queue(self):
        while not self._queue.empty():
            self._main_loop()

    def execute_queue(self, subthread=True):
        if subthread:
            threading.Thread(target=self._execute_queue).start()
        else:
            self._execute_queue()

    def _main_loop(self):
        try:
            target, args, kwargs = self._queue.get(timeout=2)
        except Empty:
            pass
        else:
            self._ḿaxthreads.start_thread(target=target,
                                          args=args,
                                          kwargs=kwargs)

    def put(self, target, args=(), kwargs={}):
        self._queue.put((target, args, kwargs))
