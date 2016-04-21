import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from maxthreads import *
from random import randint
from time import sleep

m = MaxThreads(20, prio_queue=True, thread_timeout=-5)


def p(order, prio):
    print('Queue order: ', order, 'Prio: ', prio)
    # print(threading.current_thread())
    sleep(0.1)


for i in range(200):
    rand1 = randint(0, 2)
    rand2 = randint(0, 10)
    # if i > 200:
    #     m.stop()
    m.add_task(target=p, priority=(rand1, rand2), args=(i, (rand1, rand2)))
sleep(0.1)
m.stop(block=False)