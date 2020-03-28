from multiprocessing.connection import Client
import threading

conn = Client(('localhost', 6000))

def clientSend():
    while True:
        msg = input("Enter Any message:   ")
        conn.send(msg)
def clientRecv():
    while True:
        msg = conn.recv()
        print(f"Recieved {repr(msg)}")
        
t1 = threading.Thread(target=clientSend).start()
t2 = threading.Thread(target=clientRecv).start()