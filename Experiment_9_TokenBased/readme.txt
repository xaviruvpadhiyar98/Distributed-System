Distributed monitor

The correct library is in the sk.py file

Requirements
Python 3
ZeroMQ library (pip install zmq)
Examples / Examples
Producer.py program
The program generates numbers and adds them to the shared list. After generating 20 numbers, it finishes its operation.

parameters:

Used to indicate which node will have the token first. 1 means token.
Current node address and port.
and next are the addresses of other nodes
The program consumer.py
The program retrieves numbers from the shared list and displays them. After 5 unsuccessful attempts (the list is empty), downloading the number ends.

parameters:

Current node address and port
and next are the addresses of other nodes
Producer-consumer system configuration for 2 producers and 2 consumers
Each node listens on its port and address 127.0.0.1

python3 producer.py 1 127.0.0.1:2222 127.0.0.1:3333 127.0.0.1:4444 127.0.0.1:5555
python3 producer.py 0 127.0.0.1:3333 127.0.0.1:2222 127.0.0.1:4444 127.0.0.1:5555
python3 consumer.py 127.0.0.1:4444 127.0.0.1:5555 127.0.0.1:2222 127.0.0.1:3333
python3 consumer.py 127.0.0.1:5555 127.0.0.1:4444 127.0.0.1:2222 127.0.0.1:3333
start-up
Each node is waiting for all others to run. The last node to start must be the token.
