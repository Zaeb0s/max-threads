#!/bin/env python3
import threading
from queue import Queue, Empty
from loopfunction import Loop


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
        print('THREAD STARTED')
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


# class ThreadStarter:
#     """This class can run a separate thread for the sole purpose of starting threads with MaxThreads (yeah, I know
#     very specific, but I found myself implementing this or something similar in most programs using MaxThreads)
#     This can be useful if we want to queue up functions to be started in a subthread from a thread that we don't
#     want to be blocked by the MaxThreads object.
#
#     The put funtion puts functions in a queue to be started by MaxThreads.start_thread
#
#     execute_queue
#     """
#     def __init__(self, max_threads=-1):
#         self._ḿaxthreads = MaxThreads(max_threads)
#         self._queue = Queue()
#         self._loop = Loop(target=self._main_loop)
#
#     def serve_forever(self, subthread=True):
#         self._loop.start(subthread=subthread)
#
#     def stop_serve_forever(self):
#         self._loop.stop()
#
#     def _execute_queue(self):
#         while not self._queue.empty():
#             self._main_loop()
#
#     def execute_queue(self, subthread=True):
#         if subthread:
#             threading.Thread(target=self._execute_queue).start()
#         else:
#             self._execute_queue()
#
#     def _main_loop(self):
#         try:
#             target, args, kwargs = self._queue.get(timeout=2)
#         except Empty:
#             pass
#         else:
#             self._ḿaxthreads.start_thread(target=target,
#                                           args=args,
#                                           kwargs=kwargs)
#
#     def put(self, target, args=(), kwargs={}):
#         self._queue.put((target, args, kwargs))
