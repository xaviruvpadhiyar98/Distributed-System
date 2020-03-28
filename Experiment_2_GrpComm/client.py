from socket import socket, gethostbyname

soc = socket()
host_name = gethostbyname("localhost")

name = input("Enter Your Name ")
soc.connect((host_name,8000))

print("Connected....")

soc.send(name.encode())
server_name = soc.recv(1024).decode()

print(f"{server_name} has joined ....Type Bye to End Chat")

while True:
	msg = soc.recv(1024).decode()
	print(f"{server_name} > {msg}")
	msg = input("Me >")
	if msg.lower() == 'bye':
		msg = "Leaving the Chat Room"
		soc.send(msg.encode())
		break
	soc.send(msg.encode())	
