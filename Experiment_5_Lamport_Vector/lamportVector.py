from multiprocessing import Process , Pipe
from os import getpid
from datetime import datetime
from time import sleep

def local_time(counter):
    return (f"Lamport_Time = {counter} , Local_Time = {datetime.now()}")

def calc_recv_timestamp(recv_time_stamp , counter):
    return max(recv_time_stamp, counter) + 1

def event(pid, counter):
    counter += 1
    print(f"Something happened in {pid} {local_time(counter)}!")
    return counter

def send_message(pipe , pid ,counter):
    counter += 1
    pipe.send(("Empty shell", counter))
    print(f"Message send from {pid} {local_time(counter)}")
    return counter

def recv_message(pipe , pid , counter):
    message , timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print(f"Message received from {pid} {local_time(counter)}")
    return counter

def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid , counter)
    counter = send_message(pipe12, pid ,counter)
    
    ###serially execution of lamport time counter to do 
    sleep(3)
    
    counter = event(pid, counter)
    counter = recv_message(pipe12 , pid , counter)
    counter = event(pid, counter)
    
def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe21 , pid, counter)
    counter = send_message(pipe21 , pid, counter)
    counter = send_message(pipe23 , pid, counter)
    counter = recv_message(pipe23 , pid, counter)

def process_three(pipe32):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe32 , pid ,counter)
    counter = send_message(pipe32 , pid ,counter)

oneandtwo, twoandone = Pipe()
twoandthree , threeandtwo = Pipe()

process1 = Process(target=process_one, args=(oneandtwo,))
process2 = Process(target=process_two, args=(twoandone,twoandthree))
process3 = Process(target=process_three, args=(threeandtwo,))

process1.start()
process2.start()
process3.start()

process1.join()
process2.join()
process3.join()







	
