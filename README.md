# maxthreads

Python module for limiting the number of active threads


## installation

```sh
pip install maxthreads
```

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
    thread_limiter.start_thread(target=fun)
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

## Variables of the MaxThreads.start_thread function

Variable | Description | Default
--|--|--
target | The target function | No default value
args | The arguments to be used when calling target | ()
kwargs | The keyword arguments to be used when calling target | {}

