from threading import Thread,Lock

class Counter(object):
	def __init__(self):
		self.value = 0
#		self.lock = Lock()
	def increment(self):
#		with self.lock:
#			self.value += 1
		self.value += 1
c = Counter()

def go():
	for i in range(10000):
		c.increment()
		
t1 = Thread(target=go)
t1.start()
t2 = Thread(target=go)
t2.start()

t1.join()
t2.join()
print(c.value)		

