Descriptions can be found in the markdown `README
<https://github.com/Zaeb0s/max-subthreads/blob/master/README.md>`_.

New features:

V.0.2.0
   - start_thread now returns the Thread object

V.0.3.0
  - Added ThreadStarter Class. This class can run a separate thread for the sole purpose of starting threads with MaxThreads

V.0.4.0
  - Removed ThreadStarter Class because the new way start_thread is written makes this class obsolete (it no longer blocks while waiting for a thread to become available).