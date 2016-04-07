# maxthreads

Python module for limiting the number of active threads


## installation

```sh
pip install maxthreads
```

## Version updates

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
## How to use

```python
#!/bin/env python3
import maxthreads

# Lets say you have a function "fun" you want to run within several threads at the same time.

from time import sleep
from threading import active_count
from random import random
def fun():
    print('Active threads: ', active_count())
    sleep(random()*2)


# The following initiates a MaxThreads object with the limit set to 3
thread_limiter = maxthreads.MaxThreads(3)

# The following starts 10 threads each running the fun function.
for i in range(10):
    thread_limiter.add_tast(target=fun)
```

As can be seen by the output the maximum number of threads will be 4 (The mainthread and the 3 allowed by MaxThreads

```sh
Active threads:  2
Active threads:  3
Active threads:  4
Active threads:  4
Active threads:  4
Active threads:  4
Active threads:  4
Active threads:  4
Active threads:  4
Active threads:  4

...
```

## Variables of the MaxThreads.add_tast function

Variable | Description | Default
---------|-------------|--------
target | The target function | No default value
args | The arguments to be used when calling target | ()
kwargs | The keyword arguments to be used when calling target | {}
priority | Sets priority where the highest prio is the lowest number | 0

## Priority
In order to be able to use the priority variable in MaxThreads.add_tast you must set prio_queue=True when initiating the MaxThreads object. The example above would then contruct the MaxThreads object like:
```python
thread_limiter = maxthreads.MaxThreads(3, prio_queue=True)
```

