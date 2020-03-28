#!/usr/bin/python3

import signal
import time
import sys
from sk import ExchangeObject, DistributedMonitor
import random

def ctrl_c(signal, frame):
        print('Stoping...')
        ds.stop_zmq()
        sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c)

my_id = sys.argv[1]
workers = sys.argv[1:]

ds = DistributedMonitor(my_id, False, workers)
ds.run_zmq()

i = 0  # program counter
while True:
    prod = ds.acquire()
    if prod:
        i = 0
        print("Processing:", prod.pop(0))
    else:
        print("There is nothing to process")
        i+=1
    time.sleep(random.randint(1,5))
    ds.release(prod)

    if (i>=5):
        print("Products are over")
        ds.stop_zmq()
        sys.exit(0)

    time.sleep(random.randint(1,5))
