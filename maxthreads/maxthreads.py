"""
2016-03-28: Adding priority queues
2016-03-29: Changed how MaxThreads.stop works
2016-04-04: Added a join function and removed unused modules
2016-04-05: The priority variable in SetPrio can now be a tuple
2016-04-07: Changed name of start_thread to the more accurate add_task (the old name can still be used)
2016-04-21:
- Fixed bug in the stop function where it wouldn't work if the priority variable in previously
added tasks still in the queue was anything else than an integer.
- Fixed bug in the empty_queue where it would empty the queue then block indefinitely.
- Removed start function because tasks are now deleted in the stop function.
- Added get_task_queue_count function
2016-04-26:
- Fixed bug where a new thread could close before being added to the threads list
- Fixed bug where add_task wouldn't start a new thread when it should
"""

# !/bin/env python3
import threading
from queue import Queue, Empty, PriorityQueue

__all__ = ['MaxThreads']


class Counter:
    def __init__(self):
        self.i = -1

    def __call__(self):
        self.i += 1
        return self.i

    def reset(self):
        self.i = -1


unique_id = Counter()


def DoNothing():
    pass


class SetPrio:
    def __init__(self, target, args=(), kwargs=None, priority=None):
        self.target = target
        self.priority = (priority or 0, unique_id())
        self.args = args
        self.kwargs = kwargs or {}

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __call__(self):
        self.target(*self.args, **self.kwargs)


class MaxThreads:
    def __init__(self, max_threads, thread_timeout=-1, prio_queue=False):
        """
        Args
            max_threads (int): Max number of running threads
            thread_timeout (float, int): Time (in seconds) each thread will wait for a new task before closing (<0 = stay alive)
            prio_queue (bool): whether or not to be able to prioritize tasks
        """

        if prio_queue:
            self._queue = PriorityQueue()
        else:
            self._queue = Queue()

        if thread_timeout < 0:
            self._thread_timeout = None
        else:
            self._thread_timeout = thread_timeout

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
        self._threads.append(thread)
        thread.start()
        return thread

    def add_task(self, target, args=(), kwargs=None, priority=None):
        """
        Args:
            target: A callable object to be invoked
            args: Arguments sent to the callable object upon invocation
            kwargs: Keyword arguments sent to the callable object upon invocation
            priority: Determines where to put the callable object in the list of tasks, Can be any type of object that
                is comparable using comparison operators (lower = higher priority)
        Returns:
            If a new thread was started returns the threading object otherwise returns None
        Raises:
            RuntimeError: If trying to add new task after closing object
        """

        if self._stop:
            raise RuntimeError("Can't add new task, the MaxThreads object is in closing/closed state")

        new_thread = None

        if (self.threads_active() < self._max_threads or not self._limit) \
            and (self._threads_waiting == 0 and self._queue.qsize() > 0):
            # The number of active threads is less than maximum number of threads
            # OR there is no limit on the maximum number of threads
            # AND there are no threads in waiting state
            # i.e. start a new thread
            new_thread = self._start_loop_thread()

        self._queue.put(
            SetPrio(target=target,
                    args=args,
                    kwargs=kwargs or {},
                    priority=priority or 0)
        )

        return new_thread

    def start_thread(self, target, args=(), kwargs=None, priority=0):
        """ To make sure applications work with the old name
        """
        return self.add_task(target, args, kwargs, priority)

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
        """
        Returns:
            Number of threads currently running within current object
        """
        return len(self._threads)

    def threads_waiting(self):
        """
        Returns
            Number of threads waiting for a new task
        """
        return self._threads_waiting

    def empty_queue(self):
        """ Empties the task queue
        """
        try:
            while True:
                self._queue.get(block=False)
        except Empty:
            pass

    def stop(self, block=True):
        """ Stops all active threads and rejects new tasks to be added
        Args:
            block (bool): If True, block until all threads are closed
        """
        self._stop = True

        # Removing tasks in queue
        self.empty_queue()

        # All active threads
        # With the DoNothing function
        # Because self._stop is True each thread will process at most one of the DoNothing functions
        # Hence it is ensured that all .get calls are triggered
        for _ in range(self.threads_active()):
            self._queue.put(SetPrio(target=DoNothing))

        if block:
            # Blocking until all threads are closed
            self.join()

            # Removing any leftover DoNothing functions (Can only be reliably done when all threads are closed)
            self.empty_queue()

    def join(self):
        """ Block until all active threads are closed
        """
        for thread in self._threads:
            thread.join()

    def get_task_queue_count(self):
        """
        Returns (int):
            Number of tasks waiting to be invoked
        """
        return self._queue.qsize()

