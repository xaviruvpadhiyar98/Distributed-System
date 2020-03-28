import xmlrpc.client

x = int(input("Enter First Number"))
y = int(input("Enter Second Number"))
with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
	print(f"{x} + {y} is {proxy.add(x,y)}")
