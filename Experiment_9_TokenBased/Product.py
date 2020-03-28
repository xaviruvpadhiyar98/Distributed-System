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

token = sys.argv[1]
if token == "1":
    token = True
else:
    token = False
my_id = sys.argv[2]
workers = sys.argv[2:]

ds = DistributedMonitor(my_id, token, workers)
ds.run_zmq()


i = 1  # product counter
while True:
    prod = ds.acquire()
    if not prod:
        prod = [0]
    else:
        tmp = prod[-1] + 1
        prod.append(tmp)

    print("Produces...", prod)
    i+=1
    time.sleep(random.randint(1,3))
    ds.release(prod)

    if (i >= 20):
    	print("Made:", i)
    	ds.stop_zmq()
    	sys.exit(0)

    time.sleep(random.randint(1,3))
