Descriptions can be found in the markdown `README
<https://github.com/Zaeb0s/max-subthreads/blob/master/README.md>`_.

New features:

V.0.2.0
   - start_thread now returns the Thread object

V.0.3.0
  - Added ThreadStarter Class. This class can run a separate thread for the sole purpose of starting threads with MaxThreads

V.0.4.0
  - Removed ThreadStarter Class because the new way start_thread is written makes this class obsolete (it no longer blocks while waiting for a thread to become available).

V.0.5.0
  - Added the ability to prioritize tasks started by start_thread

V.0.5.3
  - Changed how the stop function works also added a start function that can be called after stop to restart

V.0.5.8
  - The priority variable can now be a tuple

V.0.5.11
  - Changed name of start_thread to the more accurate add_task (the old name can still be used)

V.1.0.0
  - Fixed bug in the stop function where it wouldn't work if the priority variable in previously added tasks still in the queue was anything else than an integer.
  - Fixed bug in the empty_queue where it would empty the queue then block indefinitely.
  - Removed start function because tasks are now deleted in the stop function.
  - Added get_task_queue_count function

V.1.0.1
  - Fixed bug where a new thread could close before being added to the threads list
  - Fixed bug where add_task wouldn't start a new thread when it should