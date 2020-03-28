import time
import concurrent.futures

def doSomething(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f"Done Sleeping {seconds}"

secs = [5,4,3,2,1]

###Multithreading - I/O bound
start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(doSomething , secs)
    for result in results:
        print(result)
        
finish = time.perf_counter()
print(f"MultiThreading finished in {round(finish-start,2)} second(s)")

###Normal
start = time.perf_counter()
r = map(doSomething, secs)
for rs in r:
    print(rs)
finish = time.perf_counter()
print(f"Finished in {round(finish-start,2)} second(s)")