# #!/bin/env python3
#
# import maxthreads
#
# from time import sleep
# from random import random
# import threading
#
# def w():
#     print(threading.active_count())
#
#     sleep(random()*2)
#
# x = maxthreads.MaxThreads(10)
# for i in range(200):
#     x.start_thread(target=w)
#
#!/bin/env python3
import maxthreads


# Lets say you have a function "fun" you want to run within several threads at the same time.

from time import sleep
from threading import active_count
from random import random
def fun():
    print('Active threads: ', active_count())
    sleep(random()*2)


# The following initiates a MaxThreads object with the limit set to 10
thread_limiter = maxthreads.MaxThreads(3)

# The following starts 200 threads each running the fun function.
for i in range(10):
    thread_limiter.start_thread(target=fun)