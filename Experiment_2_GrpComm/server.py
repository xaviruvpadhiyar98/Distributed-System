from socket import socket,gethostbyname

soc = socket()
host_name = gethostbyname("localhost")
soc.bind((host_name, 8000))
soc.listen(100)

name = input("Enter Name ")
print("Waiting for incomming connection ....")

conn, addr = soc.accept()
print(f"Connection Established. Connected from: {addr[0]}({addr[1]})")

client_name = conn.recv(1024).decode()

print(f"{client_name} has connected")
print("Print [bye] to leave the chatroom")
conn.send(name.encode())

while True:
	msg = input("ME > ")
	if msg.lower() == 'bye':
		msg = 'Thanks See You Later'
		conn.send(msg.encode())
		print("\n")
		break
	conn.send(msg.encode())
	msg = conn.recv(1024).decode()
	print(f"{client_name} > {msg}")
	
	


