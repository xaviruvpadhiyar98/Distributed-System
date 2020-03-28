#!/usr/bin/python3

import logging
import zmq
import threading
import queue
import socket
from contextlib import closing
import time


# LOGGING SETTINGS
formatter = logging.Formatter('%(asctime)s: %(levelname)s %(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('sk.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


class ExchangeObject():
    def __init__(self, sender, receiver, mode, shared_obj, LN, Q):
        self._sender = sender
        self._receiver = receiver
        self.mode = mode  # update_RN value or token
        self.shared_obj = shared_obj
        self.LN = LN
        self.Q = Q


class DistributedMonitor():
    def __init__(self, my_id, token, workers_list):
        """
        workers_list: ip:port -> ['192.168.10.1:25', '123.123.123.123:1234']
        """

        self.__my_id = my_id
        self.__workers = workers_list  # contains self.__my_id of other nodes

        # suzuki-kasami
        self._RN = {}  # {"node1": last RN received from node1, ...}
        self._LN = {}  # {"node1": najnowszy RN dla ktorego dostep sie odbyl dla node1}
        self.Q = []  # identyfikatory czekajacych workerow
        self._token = token
        self._shared_obj = None
        self._in_CS = False
        self._RN = {x: 0 for x in self.__workers}
        self._LN = {x: 0 for x in self.__workers}

        self.__receive_queue = queue.Queue(1)  # this element will be received and pass to user (not internal communication)
        self.__running = True
        self.__lock = threading.Lock()


    ###   ZeroMQ Threads - for communicate with other workers
    def init_publisher(self):
        context_publisher = zmq.Context()
        self.publisher = context_publisher.socket(zmq.PUB)
        self.publisher.bind("tcp://%s" % (self.__my_id))


    def receive_all(self, workers):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        for worker in workers:
            subscriber.connect("tcp://%s" % worker)
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

        poller = zmq.Poller()
        poller.register(subscriber, zmq.POLLIN)

        while self.__running:
            socks = dict(poller.poll(1000)) # list of (socket, event) that is wrapped in dict {socket: event}
            if subscriber in socks:
                with self.__lock:
                    msg_obj = subscriber.recv_pyobj()  # blocking method. ExchangeObject

                    if msg_obj._sender == self.__my_id:
                        continue

                    logger.debug("%s vars_all %s" %( self.__my_id, vars(msg_obj)))
                    if msg_obj._receiver == "update_RN":
                        self._RN[msg_obj._sender] = max(self._RN[msg_obj._sender], msg_obj.mode)

                        # if i have token and im not using it and other node want token
                        if self._token and \
                                self._in_CS == False and \
                                self._RN[msg_obj._sender] == self._LN[msg_obj._sender] + 1:
                            self.send_token(msg_obj._sender)  # send token
                    elif msg_obj._receiver == self.__my_id and msg_obj.mode == "token":
                        logger.debug("%s vars_me %s" %( self.__my_id, vars(msg_obj)))
                        self.Q = msg_obj.Q
                        self._LN = msg_obj.LN
                        self.__receive_queue.put(msg_obj.shared_obj)
                        self._token = True
                    else:
                        # packet not for me
                        pass

        subscriber.close()


    def check_socket(self, host):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((host.split(":")[0], int(host.split(":")[1]))) == 0:
                return True
            else:
                return False

    def run_zmq(self):
        logger.debug("%s start" %self.__my_id)
        self.init_publisher()
        print("Waiting for all the workers to start...")

        # wait for all hosts
        tmp = [a for a in self.__workers if a != self.__my_id]
        for worker in tmp:
            while not self.check_socket(worker): time.sleep(1)


        r = threading.Thread(target=self.receive_all, args=(self.__workers,))
        r.setDaemon = True
        r.start()
        time.sleep(1)

    def stop_zmq(self):
        self.publisher.close()
        self.__running = False
    ### ---------------------------------------------

    def update_RN(self, update_val):
        msg = ExchangeObject(self.__my_id, "update_RN", update_val, None, None, None)
        self.publisher.send_pyobj(msg)

    def send_token(self, receiver):
        self._token = False
        msg = ExchangeObject(self.__my_id, receiver, "token", self._shared_obj, self._LN, self.Q)
        self.publisher.send_pyobj(msg)
        logger.debug("%s send_to %s %s %s %s" % (self.__my_id, receiver, self._shared_obj, self._LN, self.Q))


    def acquire(self):
        with self.__lock:
            logger.debug("%s acquire %s" % (self.__my_id, self._token))
            if self._token:
                # if i have token then enter into critical section
                self._in_CS = True
                return self._shared_obj
            else:
                self._RN[self.__my_id]+=1
                self.update_RN(self._RN[self.__my_id])

        self._shared_obj = self.__receive_queue.get()  # blocking method
        logger.debug("%s get %s" %(self.__my_id,self._shared_obj))
        self._in_CS = True
        return self._shared_obj

    def release(self, shared_obj):
        with self.__lock:
            logger.debug("%s release" % self.__my_id)
            self._shared_obj = shared_obj
            self._LN[self.__my_id] = self._RN[self.__my_id]

            tmp_list = [node for node in self.__workers if node not in self.Q]

            for w in tmp_list:
                if self._RN[w] == self._LN[w] + 1:
                    self.Q.append(w)
            logger.debug("%s wokers_queue %s" % (self.__my_id, self.Q))
            if self.Q:
                next_worker = self.Q.pop(0)
                self.send_token(next_worker)

            self._in_CS = False
