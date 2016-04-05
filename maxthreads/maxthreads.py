#!/bin/env python3
import threading
from queue import Queue, Empty, PriorityQueue
"""
2016-03-28: Adding priority queues
2016-03-29: Changed how MaxThreads.stop works
2016-04-04: Added a join function and removed unused modules
2016-04-05: The priority variable in SetPrio can now be a tuple
"""

class Counter:
    i = -1
    def __call__(self):
        self.i += 1
        return self.i

    def reset(self):
        self.i = -1

unique_id = Counter()

def DoNothing():
    pass

class SetPrio:
    def __init__(self, target, args=(), kwargs={}, priority=0):
        self.target = target
        if type(priority) == tuple:
            self.priority = priority + (unique_id(), )
        else:
            self.priority = (priority, unique_id())
        self.args = args
        self.kwargs = kwargs

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __lt__(self, other):
        return  self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __call__(self):
        self.target(*self.args, **self.kwargs)


class MaxThreads:
    def __init__(self, max_threads, thread_timeout=-1, prio_queue=False):
        # if type(max_threads) != int or max_threads < 1:
        #     raise ValueError('Maximum threads needs to be an integer larger than zero')

        if prio_queue:
            self._queue = PriorityQueue()
        else:
            self._queue = Queue()

        if thread_timeout < 0:
            self._thread_timeout = None
        else:
            self._thread_timeout = thread_timeout
        # if thread_timeout >= 0:
            # self._thread_timeout = thread_timeout
            # self._close_thread_on_empty = True
        # else:
            # self._thread_timeout = 2
            # self._close_thread_on_empty = False

        self._threads_active = 0
        self._threads_waiting = 0

        self._max_threads = max_threads

        if max_threads > 0:
            self._limit = True
        else:
            self._limit = False

        self._threads = []
        self._stop = False

    def _start_loop_thread(self):
        thread = threading.Thread(target=self._loop)
        thread.start()
        return thread

    def start_thread(self, target, args=(), kwargs={}, priority=0):
        if self._stop:
            raise RuntimeError("Can't start new thread, the MaxThreads is in closing/closed state")

        PrioFunction = SetPrio(target=target,
                               args=args,
                               kwargs=kwargs,
                               priority=priority)
        self._queue.put(PrioFunction)
        if (self.threads_active() < self._max_threads or not self._limit) and self._threads_waiting == 0:
            # self._threads_active += 1
            # threading.Thread(target=self._loop).start()
            self._threads.append(self._start_loop_thread())

    def _loop(self):
        serve = True
        try:
            while serve and not self._stop:
                if self._queue.qsize() == 0:
                    # Because the queue is empty it is safe to reset the
                    # Second prio number (unique id)
                    # Doing this so the unique_id won't get too big
                    unique_id.reset()

                try:
                    self._threads_waiting += 1
                    target = self._queue.get(timeout=self._thread_timeout)
                    self._threads_waiting -= 1

                except Empty:
                    self._threads_waiting -= 1
                    serve = False

                else:
                    # The args and kwargs are automatically added to the target call
                    # These are set when the target is put into the queue in the start_thread function
                    target()

        except:
            # Thread is about to crash start new _loop thread and replace current thread in _threads
            # list with the new thread

            index = self._threads.index(threading.current_thread())
            self._threads[index] = self._start_loop_thread()
            raise
        else:
            # Thread stopped normally. Remove from _threads list
            self._threads.remove(threading.current_thread())

    def threads_active(self):
        return len(self._threads)

    def threads_waiting(self):
        return self._threads_waiting

    def empty_queue(self):
        try:
            while True:
                self._queue.get()
        except Empty:
            pass

    def stop(self, block=True):
        self._stop = True

        # Next triggering all active threads
        # With the DoNothing function
        # Because self._stop is True each thread will process at most one of the DoNothing functions
        # Hence it is ensured that all .get calls are triggered
        for _ in range(self.threads_active()):
            self._queue.put(SetPrio(target=DoNothing))

        if block:
            self.join()

    def join(self):
        for thread in self._threads:
            thread.join()

    def start(self):
        if not self._stop:
            raise RuntimeError("Can't start unstopped MaxThreads object, no need to call this during startup. "
                               "Only needed when starting a stopped MaxThreads object")
        self._stop = False
        queue = self._queue

        self._queue = type(self._queue)()

        while queue.qsize() != 0:
            SetPrio_function = queue.get(block=False)
            self.start_thread(target=SetPrio_function.target,
                              args=SetPrio_function.args,
                              kwargs=SetPrio_function.kwargs,
                              priority=SetPrio_function.priority)




if __name__ == '__main__':
    from random import randint
    from time import sleep

    m = MaxThreads(10, prio_queue=True, thread_timeout=-5)
    def p(order, prio):
        print('Queue order: ', order, 'Prio: ', prio)
        # print(threading.current_thread())
        sleep(0.1)




    for i in range(200):
        rand = randint(0,2)
        m.start_thread(target=p, priority=rand, args=(i, rand))








