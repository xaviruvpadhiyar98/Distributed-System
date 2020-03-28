from multiprocessing.connection import Listener
import threading

listener = Listener(('localhost', 6000) )
conn = listener.accept()
print ('connection accepted from', listener.last_accepted)

def serverSend():
    while True:
        msg = input("Enter Any message:  ")
        conn.send(msg)
def serverRecv():
    while True:
        msg = conn.recv()
        print(f"Recieved {repr(msg)}")
        
t1 = threading.Thread(target=serverRecv).start()
t2 = threading.Thread(target=serverSend).start()




